from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import requests
import re
import cv2
import numpy as np
import duckdb
from io import BytesIO

app = FastAPI()

PARQUET_PATH = "../data/wikipedia.parquet"

def init_duckdb():
    con = duckdb.connect()
    con.sql(f"CREATE VIEW pageviews AS SELECT * FROM read_parquet('{PARQUET_PATH}')")
    return con

def get_top_articles(limit=20):
    con = init_duckdb()
    result = con.sql(f"""
        SELECT article_title, view_count
        FROM pageviews
        WHERE wiki_code = 'en.wikipedia'
          AND article_title NOT LIKE 'Special:%'
          AND article_title NOT LIKE 'Wikipedia:%'
          AND article_title NOT LIKE 'Help:%'
          AND article_title NOT LIKE 'File:%'
          AND article_title NOT LIKE 'Category:%'
          AND article_title NOT LIKE 'Portal:%'
          AND article_title NOT LIKE 'Template:%'
          AND article_title != 'Main_Page'
          AND article_title != '-'
        ORDER BY view_count DESC
        LIMIT {limit}
    """).fetchall()
    return [{"title": row[0], "views": row[1]} for row in result]

def get_agent_breakdown():
    con = init_duckdb()
    result = con.sql("""
        SELECT agent_type, SUM(view_count) AS views
        FROM pageviews
        GROUP BY agent_type
        ORDER BY views DESC
    """).fetchall()
    return [{"agent": row[0], "views": row[1]} for row in result]

def get_hourly_stats(hour_str=None):
    con = init_duckdb()
    if hour_str:
        query = f"""
            SELECT
                STRPTIME(hourly_encoded, '%Y%m%d%H') AS hour,
                SUM(view_count) AS views
            FROM pageviews
            WHERE hourly_encoded = '{hour_str}'
            GROUP BY hour
        """
    else:
        query = """
            SELECT
                STRPTIME(hourly_encoded, '%Y%m%d%H') AS hour,
                SUM(view_count) AS views
            FROM pageviews
            GROUP BY hour
            ORDER BY hour
        """
    result = con.sql(query).fetchall()
    return [{"hour": row[0].isoformat() if row[0] else None, "views": row[1]} for row in result]

@app.post("/")
async def handle_request(req: dict):
    print(f"Отримано: {req}")
    action = req.get('action')
    
    if action == 'fetch':
        url = req['url']
        regex = req.get('regex')
        resp = requests.get(url)
        headers = dict(resp.headers)
        text = resp.text
        lines = text.splitlines()
        matched = []
        if regex:
            pattern = re.compile(regex)
            for line_num, line in enumerate(lines, 1):
                if pattern.search(line):
                    matched.append({'line_number': line_num, 'content': line.strip()})
        result = {'headers': headers, 'matched_lines': matched[:100]}
        return result
    
    elif action == 'bw_image':
        url = req['url']
        img_resp = requests.get(url)
        img_array = np.frombuffer(img_resp.content, np.uint8)
        img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        _, encoded = cv2.imencode('.jpg', gray)
        return StreamingResponse(BytesIO(encoded.tobytes()), media_type="image/jpeg")
    
    elif action == 'wiki_stats':
        query_type = req.get('query_type')
        print(f"Запит wiki_stats: {query_type}")
        
        try:
            if query_type == 'top_articles':
                limit = req.get('limit', 20)
                result = get_top_articles(limit)
            elif query_type == 'agent_breakdown':
                result = get_agent_breakdown()
            elif query_type == 'hourly_stats':
                hour = req.get('hour')
                result = get_hourly_stats(hour)
            else:
                result = {"error": "Unknown query_type"}
            
            print(f"Відповідь: {str(result)[:200]}...")
            return result
        except Exception as e:
            error_msg = {"error": str(e)}
            print(f"Помилка: {error_msg}")
            raise HTTPException(status_code=500, detail=str(e))
    
    return {"error": "Unknown action"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)

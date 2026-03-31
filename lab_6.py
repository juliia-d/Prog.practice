import sqlite3
from pydantic import BaseModel, Field

class Block(BaseModel):
    hexString: str = Field(pattern=r'^0x[0-9a-fA-F]{8}$')
    id: int = Field(ge=1)
    view: int = Field(ge=0)
    desc: str = Field(min_length=1)
    img: str = Field(min_length=0)
    
    @classmethod
    def get_by_hex(cls, hexString, conn):
        cur = conn.cursor()
        cur.execute(
            "SELECT hexString, id, view, desc, img FROM BLOCKS WHERE hexString = ?",
            (hexString,)
        )
        row = cur.fetchone()
        if row:
            return cls(hexString=row[0], id=row[1], view=row[2], desc=row[3], img=row[4])
        return None

    @classmethod
    def get_all(cls, conn):
        cur = conn.cursor()
        cur.execute("SELECT hexString, id, view, desc, img FROM BLOCKS")
        rows = cur.fetchall()
        return [cls(hexString=row[0], id=row[1], view=row[2], desc=row[3], img=row[4]) for row in rows]

    def __str__(self):
        return f"Block({self.hexString}, {self.id}, {self.desc})"


class Source(BaseModel):
    id: int = Field(ge=1)
    ip_addr: str = Field(pattern=r'^(\d{1,3}\.){3}\d{1,3}$')
    country_code: str = Field(pattern=r'^[A-Z]{2}$')
    
    @classmethod
    def get_by_id(cls, id, conn):
        cur = conn.cursor()
        cur.execute("SELECT id, ip_addr, country_code FROM SOURCES WHERE id = ?", (id,))
        row = cur.fetchone()
        if row:
            return cls(id=row[0], ip_addr=row[1], country_code=row[2])
        return None

    @classmethod
    def get_all(cls, conn):
        cur = conn.cursor()
        cur.execute("SELECT id, ip_addr, country_code FROM SOURCES")
        rows = cur.fetchall()
        return [cls(id=row[0], ip_addr=row[1], country_code=row[2]) for row in rows]

    def __str__(self):
        return f"Source({self.id}, {self.ip_addr}, {self.country_code})"


class Person(BaseModel):
    id: int = Field(ge=1)
    name: str = Field(min_length=1)
    addr: str = Field(min_length=1)
    
    @classmethod
    def get_by_id(cls, id, conn):
        cur = conn.cursor()
        cur.execute("SELECT id, name, addr FROM PERSONS WHERE id = ?", (id,))
        row = cur.fetchone()
        if row:
            return cls(id=row[0], name=row[1], addr=row[2])
        return None

    @classmethod
    def get_all(cls, conn):
        cur = conn.cursor()
        cur.execute("SELECT id, name, addr FROM PERSONS")
        rows = cur.fetchall()
        return [cls(id=row[0], name=row[1], addr=row[2]) for row in rows]

    def __str__(self):
        return f"Person({self.id}, {self.name})"


class Vote(BaseModel):
    block_id: str = Field(pattern=r'^0x[0-9a-fA-F]{8}$')
    voter_id: int = Field(ge=1)
    timestamp: str = Field(pattern=r'^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$')
    source_id: int = Field(ge=1)
    
    @classmethod
    def get_by_block_and_voter(cls, block_id, voter_id, conn):
        cur = conn.cursor()
        cur.execute(
            "SELECT block_id, voter_id, timestamp, source_id FROM VOTES WHERE block_id = ? AND voter_id = ?",
            (block_id, voter_id)
        )
        row = cur.fetchone()
        if row:
            return cls(block_id=row[0], voter_id=row[1], timestamp=row[2], source_id=row[3])
        return None

    @classmethod
    def get_all(cls, conn):
        cur = conn.cursor()
        cur.execute("SELECT block_id, voter_id, timestamp, source_id FROM VOTES")
        rows = cur.fetchall()
        return [cls(block_id=row[0], voter_id=row[1], timestamp=row[2], source_id=row[3]) for row in rows]

    @classmethod
    def get_full_details(cls, block_id, voter_id, conn):
        cur = conn.cursor()
        cur.execute("""
            SELECT v.block_id, v.voter_id, v.timestamp, v.source_id,
                   b.view, b.desc,
                   p.name, p.addr,
                   s.ip_addr, s.country_code
            FROM VOTES v
            LEFT JOIN BLOCKS b ON v.block_id = b.hexString
            LEFT JOIN PERSONS p ON v.voter_id = p.id
            LEFT JOIN SOURCES s ON v.source_id = s.id
            WHERE v.block_id = ? AND v.voter_id = ?
        """, (block_id, voter_id))
        row = cur.fetchone()
        if row:
            return {
                'block_id': row[0],
                'voter_id': row[1],
                'timestamp': row[2],
                'source_id': row[3],
                'block_view': row[4],
                'block_desc': row[5],
                'voter_name': row[6],
                'voter_addr': row[7],
                'source_ip': row[8],
                'source_country': row[9]
            }
        return None

    def __str__(self):
        return f"Vote({self.block_id}, {self.voter_id}, {self.timestamp})"

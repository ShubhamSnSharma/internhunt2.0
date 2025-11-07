# API services module for job recommendations
import requests
import json
import streamlit as st
import os
from typing import List, Dict, Optional
from urllib.parse import urlencode, quote
from config import Config

class JobAPIService:
    """Handles job API integrations"""
    
    @staticmethod
    def fetch_jobs_from_jooble(skills: List[str], location: str = "") -> Optional[List[Dict]]:
        """Fetch jobs from Jooble API"""
        url = f"https://jooble.org/api/{Config.JOOBLE_API_KEY}"
        
        # Combine all skills into a single search query
        keywords = ", ".join([s for s in (skills or []) if s])
        
        headers = {"Content-Type": "application/json"}
        
        try:
            all_jobs: List[Dict] = []
            # Fetch first two pages to ensure enough results (Jooble paginates)
            for pg in (1, 2):
                payload = {
                    "keywords": keywords,
                    "location": location or "",
                    "page": pg
                }
                response = requests.post(url, headers=headers, data=json.dumps(payload), timeout=10)
                if response.status_code != 200:
                    continue
                page_jobs = response.json().get("jobs", [])
                if page_jobs:
                    all_jobs.extend(page_jobs)
            jobs = all_jobs[:10]
            return jobs if jobs else None
        
        except requests.exceptions.RequestException as e:
            st.error(f"Jooble API request failed: {e}")
            return None
        except Exception as e:
            st.error(f"Unexpected error with Jooble API: {e}")
            return None

    @staticmethod
    def fetch_internships_from_internshala(skills: List[str], city: str = "India") -> Optional[List[Dict]]:
        """Fetch internships directly from Internshala public API (no keys required)."""
        query = ", ".join([s for s in (skills or []) if s])
        return fetch_internshala_internships(query, city)


class YouTubeService:
    """Handles YouTube video information fetching"""
    
    @staticmethod
    def fetch_yt_video(link: str) -> str:
        """Fetch YouTube video title"""
        try:
            with yt_dlp.YoutubeDL({}) as ydl:
                info = ydl.extract_info(link, download=False)
                return info.get('title', 'Unknown Title')
        except Exception as e:
            return f"Error fetching video: {e}"

# Public helper (no env required)
def fetch_internshala_internships(query: str, location: str = "India") -> Optional[List[Dict]]:
    """Fetch internships from Internshala's public search API and return a list.
    Endpoint: https://internshala.com/api/internships/search?keywords={query}&location={location}
    Strategy:
      1) Full query
      2) First keyword only
      3) Empty query for given location
      4) Fallback keyword sweep across popular fresher domains until we have 10
    """
    def _hit(q: str, loc: str) -> Optional[List[Dict]]:
        q_enc = quote((q or "").strip())
        loc_enc = quote((loc or "India").strip())
        url = f"https://internshala.com/api/internships/search?keywords={q_enc}&location={loc_enc}"
        headers = {
            "Accept": "application/json",
            "Accept-Language": "en-US,en;q=0.9",
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36",
            "Referer": "https://internshala.com/"
        }
        r = requests.get(url, timeout=10, headers=headers)
        if r.status_code != 200:
            return None
        try:
            data = r.json()
        except Exception:
            return None
        items = data.get('internships') or data.get('data') or data.get('results') or data
        if not isinstance(items, list):
            return None
        return items if items else None

    try:
        collected: List[Dict] = []
        seen = set()
        def _add(items: Optional[List[Dict]]):
            nonlocal collected, seen
            for it in (items or []):
                link = it.get('link') or it.get('url') or json.dumps(it, sort_keys=True)
                if link in seen:
                    continue
                seen.add(link)
                collected.append(it)

        # Attempt 1: full query
        res = _hit(query, location)
        _add(res)
        if len(collected) >= 10:
            return collected[:10]

        # Attempt 2: first keyword only
        first_kw = None
        if query:
            parts = [p.strip() for p in query.split(',') if p.strip()]
            first_kw = parts[0] if parts else None
        if first_kw:
            _add(_hit(first_kw, location))
            if len(collected) >= 10:
                return collected[:10]

        # Attempt 3: empty query for generic internships in location
        _add(_hit("", location))
        if len(collected) >= 10:
            return collected[:10]

        # Attempt 4: popular fresher domains sweep
        fallback_keywords = [
            "software development", "web development", "frontend", "backend",
            "python", "java", "data analyst", "data science", "machine learning",
            "android", "ios", "ui ux", "product management", "qa testing"
        ]
        fallback_locations = [location or "India", "India", ""]
        for fk in fallback_keywords:
            for fl in fallback_locations:
                _add(_hit(fk, fl))
                if len(collected) >= 10:
                    return collected[:10]
        return collected[:10] if collected else None
    except requests.exceptions.RequestException as e:
        st.warning(f"Internshala API request failed: {e}")
        return None
    except Exception as e:
        st.warning(f"Internshala API error: {e}")
        return None

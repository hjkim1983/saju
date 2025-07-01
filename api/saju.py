from datetime import datetime
from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import json

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        query = parse_qs(urlparse(self.path).query)
        birth = query.get("birth", [""])[0]
        gender = query.get("gender", [""])[0]

        birth_date = datetime.strptime(birth, "%Y-%m-%d")
        solar_term_date = datetime(birth_date.year, 2, 4)

        year_stem = birth_date.year % 10
        is_yang = year_stem % 2 == 0
        is_male = gender.lower() == "male"
        is_forward = (is_male and is_yang) or (not is_male and not is_yang)

        days_diff = abs((solar_term_date - birth_date).days)
        start_age = int(days_diff / 3)

        result = {
            "입력값": {"birth": birth, "gender": gender},
            "대운방향": "순행" if is_forward else "역행",
            "대운시작나이": start_age,
            "기준절기": solar_term_date.strftime("%Y-%m-%d")
        }

        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(result).encode())

import requests
from typing import Iterable
import json


def get_size(url: str) -> int:
    r = requests.get(url).json()
    found = r.get("pages")
    return found


def parse_page(url, pages: Iterable) -> list[dict]:
    result = []
    for page in pages:
        print(f"----страница {page + 1}")
        r = requests.get(url + f"&page={page}").json()
        vacancy = r.get("items")
        v = filter(lambda x: parse_text(x), vacancy)
        page_data = []
        for record in v:
            salary = record.get("salary")
            if not salary:
                salary = "Не указана"
            else:
                salary = (f'{record.get("salary").get("from")} - {record.get("salary").get("to")} '
                          f'{record.get("salary").get("currency")}')
            json_data = {"link": record.get("alternate_url"),
                         "salary": salary,
                         "employer": record.get("employer").get("name"),
                         "city": record.get("area").get("name")}
            page_data.append(json_data)
        result.extend(page_data)
    return result


def parse_text(vac: dict) -> bool:
    payload = vac.get("snippet").get("requirement")
    if payload:
        a = "django" in payload.lower()
        b = "flask" in payload.lower()
        return a or b


if __name__ == "__main__":
    url = "https://api.hh.ru/vacancies?text=python&area=1&area=2&per_page=100"
    row_data = get_size(url)
    j_data = parse_page(url, range(row_data))
    print(f"Всего найдено {len(j_data)} подходящих вакансий")
    with open("sample.json", "w") as outfile:
        json.dump(j_data, outfile, ensure_ascii=False, indent=4)

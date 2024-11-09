import requests
import json

class GraphAPI:
    def __init__(self, fb_api):
        self.base_url = "https://graph.facebook.com/v21.0/"
        self.token = fb_api

    def get_insights(self, ad_acc, specific_date=None):
        insights_data = []

        insights_fields = [
            "ad_id",
            "adset_id",
            "campaign_id",
            "campaign_name",
            "adset_name",
            "ad_name",
            "date_start",
            "date_stop",
            "reach",
            "impressions",
            "clicks",
            "inline_link_clicks",
            "ctr",
            "spend",
            "cost_per_action_type",
            "actions",
            "action_values",
            "quality_ranking",
            "engagement_rate_ranking",
            "cpm",
            "cpc",
        ]

        url = f"{self.base_url}act_{ad_acc}/insights?level=ad&fields={','.join(insights_fields)}&access_token={self.token}"

        if specific_date:
            url += f"&time_range={{'since':'{specific_date}','until':'{specific_date}'}}"
        else:
            url += "&date_preset=today"

        url += "&action_breakdowns=action_type"

        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            insights_list = data.get("data", [])
        else:
            print(f"Erro ao obter insights: {response.status_code} - {response.text}")
            return []

        adset_ids = set()
        campaign_ids = set()
        ad_ids = set()

        for entry in insights_list:
            adset_id = entry.get('adset_id')
            campaign_id = entry.get('campaign_id')
            ad_id = entry.get('ad_id')
            if adset_id:
                adset_ids.add(adset_id)
            if campaign_id:
                campaign_ids.add(campaign_id)
            if ad_id:
                ad_ids.add(ad_id)

        def fetch_objects_data(object_ids, fields, object_type):
            objects_data = {}
            object_ids_list = list(object_ids)
            for i in range(0, len(object_ids_list), 50):
                batch_ids = object_ids_list[i:i+50]
                ids_param = ','.join(batch_ids)
                url = f"{self.base_url}?ids={ids_param}&fields={','.join(fields)}&access_token={self.token}"
                response = requests.get(url)
                if response.status_code == 200:
                    data = response.json()
                    objects_data.update(data)
                else:
                    print(f"Erro ao obter dados de {object_type}: {response.status_code} - {response.text}")
            return objects_data

        adsets_fields = ["id", "name", "bid_strategy", "daily_budget", "lifetime_budget", "start_time", "end_time"]
        adsets_data = fetch_objects_data(adset_ids, adsets_fields, "conjuntos de anúncios")

        campaigns_fields = ["id", "name", "objective", "start_time", "stop_time", "bid_strategy"]
        campaigns_data = fetch_objects_data(campaign_ids, campaigns_fields, "campanhas")

        ads_fields = ["id", "name", "created_time", "effective_status"]
        ads_data = fetch_objects_data(ad_ids, ads_fields, "anúncios")

        for entry in insights_list:
            row = {}

            ad_id = entry.get("ad_id")
            adset_id = entry.get("adset_id")
            campaign_id = entry.get("campaign_id")

            row["Nome da campanha"] = entry.get("campaign_name")
            row["Nome do conjunto de anúncios"] = entry.get("adset_name")
            row["Nome do anúncio"] = entry.get("ad_name")

            row["Data de início"] = entry.get("date_start")
            row["Data de término"] = entry.get("date_stop")

            campaign = campaigns_data.get(campaign_id, {})
            row["Objetivo"] = campaign.get("objective")
            row["Data de início da campanha"] = campaign.get("start_time")
            row["Data de término da campanha"] = campaign.get("stop_time")
            row["Estratégia de lance da campanha"] = campaign.get("bid_strategy")

            adset = adsets_data.get(adset_id, {})
            row["Estratégia de lançamento"] = adset.get("bid_strategy")
            budget = adset.get("daily_budget") or adset.get("lifetime_budget")
            if budget:
                budget = float(budget) / 100
            else:
                budget = 0.0
            row["Orçamento"] = budget
            row["Data de início do conjunto de anúncios"] = adset.get("start_time")
            row["Data de término do conjunto de anúncios"] = adset.get("end_time")

            ad = ads_data.get(ad_id, {})
            row["Data de criação do anúncio"] = ad.get("created_time")
            row["Status do anúncio"] = ad.get("effective_status")

            row["Alcance"] = entry.get("reach")
            row["Impressões"] = entry.get("impressions")
            row["Cliques"] = entry.get("clicks")
            row["Cliques no link"] = entry.get("inline_link_clicks")
            row["CTR"] = entry.get("ctr")
            spend = entry.get("spend")
            if spend:
                spend = float(spend)
            else:
                spend = 0.0
            row["Valor usado"] = spend
            row["Custo por resultado"] = entry.get("cost_per_action_type")
            row["Classificação de qualidade"] = entry.get("quality_ranking")
            row["Classificação de taxa de engajamento"] = entry.get("engagement_rate_ranking")
            row["CPM"] = entry.get("cpm")
            row["CPC"] = entry.get("cpc")

            row["Action Values"] = entry.get("action_values", [])

            if specific_date:
                row["Data da consulta"] = specific_date
            else:
                row["Data da consulta"] = "today"

            insights_data.append(row)

        return insights_data

    def save_to_json(self, insights_data, output_file="insights_structured.txt"):
        if insights_data:
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(insights_data, f, ensure_ascii=False, indent=4)
            print(f"Dados exportados com sucesso para {output_file}")
        else:
            print("Nenhum dado para exportar.")

if __name__ == "__main__":
    fb_api = open("Token/fb_token.py").read().strip()
    ad_acc = "2338511086377745"

    graph_api = GraphAPI(fb_api)
    specific_date = "2024-10-30" 
    
    insights = graph_api.get_insights(ad_acc, specific_date=specific_date)
    graph_api.save_to_json(insights, output_file="API_FINAL/SAIDAS/SAIDA_API_PERFORMANCE_VIVARA_&_MGI.txt")
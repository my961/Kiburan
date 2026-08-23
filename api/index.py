def get_ai_response(user_text):
    try:
        # በነፃ የሚሰራ ክፍት የ AI API አድራሻ
        url = "https://text.pollinations.ai/" + requests.utils.quote(user_text) + "?model=openai&system=You+are+a+helpful+smart+AI+assistant.+Answer+accurately+in+Amharic+or+English."
        res = requests.get(url, timeout=12)
        if res.status_code == 200 and res.text.strip():
            return res.text
        return "⚠️ ይቅርታ፣ መልሱን ማዘጋጀት አልተቻለም።"
    except Exception:
        return "⚠️ ይቅርታ፣ መልሱን ማዘጋጀት አልተቻለም። እባክዎን ትንሽ ቆይተው ድጋሚ ይሞክሩ።"

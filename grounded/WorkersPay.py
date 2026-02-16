import requests

api_key = "4j9Ua9pp92G1xRlTQHnzLMFlkdjBeQvY"
ticker = "AMZN"

# 1. Pull the CEO's Pay
exec_data = requests.get(f"https://financialmodelingprep.com/stable/governance-executive-compensation?symbol={ticker}&apikey={api_key}").json()

ceoData = []
for ex in exec_data:
    ceo = ['Chief Executive Officer','CEO']

    for name in ceo:
        if name in ex['nameAndPosition']:
            ceoData.append(ex)
            break

ceo_pay = ceoData[0]['total']

emp_data = requests.get(f"https://financialmodelingprep.com/stable/employee-count?symbol={ticker}&apikey={api_key}").json()
emp_count = emp_data[0]['employeeCount']


inc_data = requests.get(f"https://financialmodelingprep.com/stable/income-statement?symbol={ticker}&apikey={api_key}").json()

sga_expense = inc_data[0]['sellingGeneralAndAdministrativeExpenses']

url = f"https://financialmodelingprep.com/stable/profile?symbol={ticker}&apikey={api_key}"
inc_data = requests.get(url).json()
emp_count = int(inc_data[0]['fullTimeEmployees'])

avg_worker_cost = sga_expense / emp_count
ratio = ceo_pay / avg_worker_cost

print(f"{ticker} CEO Pay: ${ceo_pay:,}")
print(f"Estimated Avg Worker Cost: ${avg_worker_cost:,.2f}")
print(f"CEO-to-Worker Ratio: {ratio:.1f}x")
import json
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException


def access_platform(driver):
    driver.get("https://procesosjudiciales.funcionjudicial.gob.ec/")


def basic_search(driver, document):
    try:
        # Basic Search
        input_element = driver.find_element(By.XPATH, '//*[@id="texto"]')
        input_element.click()
        input_element.send_keys(document)

        search_button = driver.find_element(
            By.XPATH, "/html/body/app-root/app-expel-busqueda-inteligente/section/section/div[3]/div/form/div[1]/div/button")
        search_button.click()

    except NoSuchElementException:
        print("Search element not found. Verify the XPath selector.")
        return None


def advanced_search(driver, document, filter):
    """
        Performs an advanced search based on the given criteria.
        Args:
            driver (selenium.webdriver): The Selenium WebDriver instance.
            document (str): The document number to search for.
            filter (str): The filter option to determine the type of search to perform.

        Returns:
            None

        Raises:
            NoSuchElementException: If the search element is not found.

        Notes:
            This function performs an advanced search on a web page using the Selenium WebDriver.
            It clicks on the advanced search button and then executes the corresponding search option based on
            the provided filter. The options dictionary maps the filter to the corresponding search
            function. If the filter is not valid, an error message is printed. If the search element
            is not found, a NoSuchElementException is raised.

        Example:
            advanced_search(driver, "1234567890", "plaintiff")
    """
    try:
        # Advanced Search
        search_button = driver.find_element(
            By.XPATH, "/html/body/app-root/app-expel-busqueda-inteligente/section/section/div[3]/div/div/button")
        search_button.click()
        options = {
            "plaintiff": search_plaintiff,
            "defendant": search_defendant
        }

        # Execute the corresponding option
        if filter in options:
            return options[filter](driver, document, filter)
        else:
            print("Invalid option.")

    except NoSuchElementException:
        print("Search element not found. Verify the XPath selector.")
        return None


def search_plaintiff(driver, document, type):
    try:
        input_element = driver.find_element(By.ID, "mat-input-2")
        input_element.click()
        input_element.send_keys(document)

        url = "https://api.funcionjudicial.gob.ec/EXPEL-CONSULTA-CAUSAS-SERVICE/api/consulta-causas/informacion/buscarCausas?page=1&size=10000"
        payload = {
            "actor": {
                "cedulaActor": document,
                "nombreActor": ""
            },
            "demandado": {
                "cedulaDemandado": "",
                "nombreDemandado": ""
            },
            "recaptcha": "verdad"
        }
        processes = make_request(url, payload)
        get_process_details(processes, document, type)
        return processes

    except NoSuchElementException:
        print("Element not found. Verify the XPath selector.")
        return None


def search_defendant(driver, document, type):
    try:
        input_element = driver.find_element(By.ID, "mat-input-4")
        input_element.click()
        input_element.send_keys(document)

        url = "https://api.funcionjudicial.gob.ec/EXPEL-CONSULTA-CAUSAS-SERVICE/api/consulta-causas/informacion/buscarCausas?page=1&size=10000"
        payload = {
            "actor": {
                "cedulaActor": "",
                "nombreActor": ""
            },
            "demandado": {
                "cedulaDemandado": document,
                "nombreDemandado": ""
            },
            "recaptcha": "verdad"
        }
        processes = make_request(url, payload)
        get_process_details(processes, document,type)
        return processes
    except NoSuchElementException:
        print("Element not found. Verify the XPath selector.")
        return None


def get_process_details(processes, document, type):
    print(f"Extracting process details for document {document}")

    with ThreadPoolExecutor() as executor:
        process_futures = {executor.submit(
            get_process_details_helper, process): process for process in processes}
        for future in as_completed(process_futures):
            process = process_futures[future]
            response = future.result()
            process['documento']=document
            process['type']=type
            process["detalles"] = response.json(
            ) if response.status_code == 200 else None
            executor.submit(get_judicial_proceedings, process,
                            process["detalles"], document)


def get_process_details_helper(process):
    url = f"https://api.funcionjudicial.gob.ec/EXPEL-CONSULTA-CAUSAS-CLEX-SERVICE/api/consulta-causas-clex/informacion/getIncidenteJudicatura/{process['idJuicio']}"
    response = requests.get(url)
    return response


def get_judicial_proceedings(process, details, document):
    print(f"Extracting judicial proceedings for process {process['id']}")
    url = "https://api.funcionjudicial.gob.ec/EXPEL-CONSULTA-CAUSAS-SERVICE/api/consulta-causas/informacion/actuacionesJudiciales"

    # Access list elements by their index
    id_movimiento = details[0]['lstIncidenteJudicatura'][0]['idMovimientoJuicioIncidente']
    id_incidente = details[0]['lstIncidenteJudicatura'][0]['idIncidenteJudicatura']

    payload = {
        "idMovimientoJuicioIncidente": id_movimiento,
        "idJuicio": process['idJuicio'],
        "idJudicatura": details[0]['idJudicatura'],
        "idIncidenteJudicatura": id_incidente
    }

    response = requests.post(url, json=payload)
    process['actuaciones'] = response.json(
    ) if response.status_code == 200 else None


def make_request(url, payload):
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print("Error making request:", e)
        return None


def search_processes(driver, document, type):
    access_platform(driver)
    return advanced_search(driver, document, type)


def initialize_driver():
    options = webdriver.ChromeOptions()
    # Ejecución sin abrir una ventana del navegador
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)
    return driver


def close_driver(driver):
    driver.quit()


def search_and_save_processes(driver, documents, type):
    results = []
    for document in documents:
        print(f"Searching processes for {type}: {document}")
        results.extend(search_processes(driver, document, type))
        print("--------------------")
    return results


def save_results(results):
    with open("process_db.json", "w") as f:
        json.dump(results, f, indent=4)
    print("Data extracted and saved succesfully")
    

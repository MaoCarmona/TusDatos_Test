from process import * 


def main():
    try:
        # Initialize the Selenium WebDriver
        driver = initialize_driver()

        # Documents to search for
        plaintiff = ["0968599020001", "0992339411001"]
        defendant = ["1791251237001", "0968599020001"]

        # Perform the search and save the results for each type of document
        results = {}
        results.update(search_and_save_processes(
            driver, plaintiff, "plaintiff"))
        results.update(search_and_save_processes(
            driver, defendant, "defendant"))

        # Save results to a JSON file
        save_results(results)

    except Exception as e:
        print("An error occurred during execution:", e)

    finally:
        # Close the driver when finished
        close_driver(driver)


if __name__ == "__main__":
    main()

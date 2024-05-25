package helpers

import io.qameta.allure.Allure
import io.qameta.allure.model.TestResult

object AllureHelper {

    // This method updates the test name for the Allure report
    // It appends the provided parameter to the test name
    fun updateTestNameForAllureReport(param: String) {
        val lifecycle = Allure.getLifecycle()
        lifecycle.updateTestCase { testResult: TestResult ->
            testResult.name += param
        }
    }

}
package helpers

import io.qameta.allure.Allure
import io.qameta.allure.model.TestResult

object AllureHelper {

    fun updateTestNameForAllureReport(param: String) {
        val lifecycle = Allure.getLifecycle()
        lifecycle.updateTestCase { testResult: TestResult ->
            testResult.name += param
        }
    }

}
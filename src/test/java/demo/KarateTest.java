package demo;

import com.intuit.karate.junit5.Karate;

class KarateTest {
    @Karate.Test
    Karate backendFeatures() {
        return Karate.run("classpath:backend");
    }
}

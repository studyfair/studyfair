package ru.spbu.detector.detection;

import java.util.Map;

public class LCSDetectorParams extends DetectionAlgorithmParameters {
    private final double threshold;
    private final int n;

    public LCSDetectorParams(Map<String, Object> params) {
        // TODO Что если Map не содержит таких полей? Куда доставлять ошибку
        n = (int) params.get("n");
        threshold = (double) params.get("threshold");
    }

    public double getThreshold() {
        return threshold;
    }

    public int getN() {
        return n;
    }
}

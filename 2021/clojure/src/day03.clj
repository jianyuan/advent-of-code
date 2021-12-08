(ns day03
  (:require [clojure.string :as str]
            [utils :refer [parse-integer]]))

(def input
  (->> "data/day03.txt"
       slurp
       str/split-lines))

(defn frequencies-by [xs pred]
  (let [transposed (apply mapv vector xs)
        n (/ (count xs) 2)]
    (mapv (fn [ys]
            (let [freq (->> ys
                            frequencies
                            (sort-by val pred)
                            first)]
              (if (= n (val freq))
                (if (= pred >)
                  \1
                  \0)
                (key freq))))
          transposed)))

(defn gamma-rate [xs]
  (parse-integer 2 (frequencies-by xs >)))

(defn epsilon-rate [xs]
  (parse-integer 2 (frequencies-by xs <)))

(defn generator-rating [xs pred]
  (parse-integer 2
                 (loop [ys xs
                        index 0]
                   (let [n (nth (frequencies-by ys pred) index)
                         zs (filter #(= n (nth % index)) ys)]
                     (if (= 1 (count zs))
                       (first zs)
                       (recur zs (inc index)))))))

(defn oxygen-generator-rating [xs]
  (generator-rating xs >))

(defn co2-generator-rating [xs]
  (generator-rating xs <))

(defn part1 []
  (* (gamma-rate input) (epsilon-rate input)))

(defn part2 []
  (* (oxygen-generator-rating input) (co2-generator-rating input)))

(do
  (println "Part 1:" (part1))
  (println "Part 2:" (part2)))

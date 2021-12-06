(ns day03
  (:require [clojure.string :as str]
            [utils :refer [parse-integer]]))


(def input
  (->> "data/day03.txt"
       slurp
       str/split-lines
       (apply mapv vector)))

(defn frequencies-by [pred xs]
  (->> xs
       frequencies
       (sort-by val pred)
       first
       key))

(defn gamma-rate [xs]
  (->> xs
       (map #(frequencies-by > %))
       (parse-integer 2)))

(defn epsilon-rate [xs]
  (->> xs
       (map #(frequencies-by < %))
       (parse-integer 2)))

(defn part1 []
  (* (gamma-rate input) (epsilon-rate input)))

(do (println "Part 1:" (part1)))

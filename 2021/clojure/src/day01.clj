(ns day01
  (:require [clojure.string :as str]))

(def input
  (->> "data/day01.txt"
       slurp
       str/split-lines
       (map #(Integer/parseInt %))))

(defn count-increasing [numbers]
  (->> numbers
       (partition 2 1)
       (filter #(apply < %))
       (count)))

(defn part1 []
  (count-increasing input))

(defn part2 []
  (->> input
       (partition 3 1)
       (map #(apply + %))
       (count-increasing)))

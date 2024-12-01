(ns day01
  (:require
   [clojure.string :as str]))

(defn parse-input [file-path]
  (let [lines (str/split-lines (slurp file-path))]
    (map (fn [line]
           (let [[x y] (str/split line #"\s+")]
             [(Integer/parseInt x) (Integer/parseInt y)]))
         lines)))

(defn transpose [pairs]
  (apply map vector pairs))

(defn sort-transposed [transposed]
  (map sort transposed))

(defn zip-and-difference [transposed]
  (map (fn [[x y]] (abs (- y x))) (apply map vector transposed)))

(defn sum [numbers]
  (reduce + numbers))

(defn frequency-map [numbers]
  (reduce (fn [freq-map item]
            (update freq-map item (fnil inc 0)))
          {}
          numbers))

(defn multiply-by-frequency [transposed]
  (let [[list1 list2] transposed
        freq-map (frequency-map list2)]
    (map (fn [x] (* x (get freq-map x 0))) list1)))

(def parsed (parse-input "data/day01.txt"))
(def transposed (transpose parsed))
(def sorted-transposed (sort-transposed transposed))
(def differences (zip-and-difference sorted-transposed))

(let [answer (sum differences)]
  (println "Part 1:" answer))

(let [results (multiply-by-frequency transposed)
      answer (sum results)]
  (println "Part 2:" answer))

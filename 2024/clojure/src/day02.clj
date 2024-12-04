(ns day02
  (:require
   [clojure.string :as str]))

(defn parse-input [file-path]
  (->> (slurp file-path)
       str/split-lines
       (map (fn [line]
              (->> (str/split line #"\s+")
                   (map Integer/parseInt)
                   vec)))))

(defn is-safe [numbers]
  (let [pairs (partition 2 1 numbers)
        diffs (map (fn [[a b]] (- b a)) pairs)]
    (and
     (every? #(or (<= -3 % -1) (<= 1 % 3)) diffs)
     (or (every? pos? diffs) (every? neg? diffs)))))

(defn is-safe-with-dampener [numbers]
  (or
   (is-safe numbers)
   (some (fn [i]
           (is-safe (concat (subvec numbers 0 i) (subvec numbers (inc i)))))
         (range (count numbers)))))

(def parsed (parse-input "data/day02.txt"))

(let [answer (count (filter is-safe parsed))]
  (println "Part 1:" answer))

(let [answer (count (filter is-safe-with-dampener parsed))]
  (println "Part 2:" answer))

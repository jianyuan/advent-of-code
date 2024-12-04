(ns day04
  (:require
   [clojure.string :as str]))

(def directions
  [[0 1]
   [1 0]
   [1 1]
   [1 -1]
   [0 -1]
   [-1 0]
   [-1 -1]
   [-1 1]])

(defn in-bounds? [grid x y]
  (and (>= x 0)
       (< x (count grid))
       (>= y 0)
       (< y (count (first grid)))))

(defn get-letter [grid x y]
  (when (in-bounds? grid x y)
    (get-in grid [x y])))

(defn search-xmas [grid x y dx dy]
  (let [word "XMAS"
        letters (map #(get-letter grid (+ x (* dx %)) (+ y (* dy %))) (range (count word)))]
    (if (= (seq word) letters) 1 0)))

(defn count-xmas [grid]
  (reduce
   (fn [total [x y]]
     (+ total
        (reduce
         (fn [dir-total [dx dy]]
           (+ dir-total (search-xmas grid x y dx dy)))
         0
         directions)))
   0
   (for [x (range (count grid))
         y (range (count (first grid)))]
     [x y])))

(defn check-x-mas [grid x y]
  (let [diag1 (map #(get-letter grid (+ x %) (+ y %)) [0 1 2])
        diag2 (map #(get-letter grid (- (+ x 2) %) (+ y %)) [0 1 2])]
    (if (and
         (or (= diag1 (seq "MAS")) (= diag1 (seq "SAM")))
         (or (= diag2 (seq "MAS")) (= diag2 (seq "SAM"))))
      1
      0)))

(defn count-x-mas [grid]
  (reduce
   (fn [total [x y]]
     (+ total (check-x-mas grid x y)))
   0
   (for [x (range (count grid))
         y (range (count (first grid)))]
     [x y])))

(defn parse-input [input]
  (mapv vec (str/split-lines input)))

(let [input "MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX"
      parsed-input (parse-input input)]
  (println "Part 1 (Example):" (count-xmas parsed-input))
  (println "Part 2 (Example):" (count-x-mas parsed-input)))

(let [input (slurp "data/day04.txt")
      parsed-input (parse-input input)]
  (println "Part 1:" (count-xmas parsed-input))
  (println "Part 1:" (count-x-mas parsed-input)))

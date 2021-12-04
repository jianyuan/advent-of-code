(ns day02
  (:require [clojure.string :as str]))

(defrecord Instruction [direction value])
(defrecord Position [horizontal depth aim])

(defn parse-instruction [line]
  (let [[direction value] (str/split line #" ")]
    (Instruction. (keyword direction) (Integer/parseInt value))))

(def input
  (->> "data/day02.txt"
       slurp
       str/split-lines
       (map parse-instruction)))

(defn next-position [position instruction]
  (let [horizontal (:horizontal position)
        depth (:depth position)
        direction (:direction instruction)
        value (:value instruction)]
    (case direction
      :forward (assoc position :horizontal (+ horizontal value))
      :down (assoc position :depth (+ depth value))
      :up (assoc position :depth (- depth value)))))

(defn next-position-2 [position instruction]
  (let [horizontal (:horizontal position)
        depth (:depth position)
        aim (:aim position)
        direction (:direction instruction)
        value (:value instruction)]
    (case direction
      :forward (assoc position
                      :horizontal (+ horizontal value)
                      :depth (+ depth (* aim value)))
      :down (assoc position :aim (+ aim value))
      :up (assoc position :aim (- aim value)))))

(defn answer [position]
  (* (:horizontal position) (:depth position)))

(defn part1 []
  (->> input
       (reduce next-position (Position. 0 0 0))
       answer))

(defn part2 []
  (->> input
       (reduce next-position-2 (Position. 0 0 0))
       answer))

(do (println "Part 1:" (part1))
    (println "Part 2:" (part2)))

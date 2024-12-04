(ns day03)

(defn parse-and-sum-muls [input]
  (let [pattern #"mul\((\d{1,3}),(\d{1,3})\)"
        matches (re-seq pattern input)]
    (reduce
     (fn [sum [_ x y]]
       (+ sum (* (Integer/parseInt x) (Integer/parseInt y))))
     0
     matches)))

(defn parse-and-sum-muls-with-conditions [input]
  (let [mul-pattern #"mul\((\d{1,3}),(\d{1,3})\)"
        do-pattern #"do\(\)"
        dont-pattern #"don't\(\)"
        tokens (re-seq (re-pattern (str mul-pattern "|" do-pattern "|" dont-pattern)) input)]
    (:sum
     (reduce
      (fn [state [token]]
        (cond
          (re-matches (re-pattern do-pattern) token)
          (assoc state :enabled true)

          (re-matches (re-pattern dont-pattern) token)
          (assoc state :enabled false)

          (re-matches (re-pattern mul-pattern) token)
          (let [[_ x y] (re-matches (re-pattern mul-pattern) token)]
            (if (:enabled state)
              (update state :sum + (* (Integer/parseInt x) (Integer/parseInt y)))
              state))))
      {:enabled true :sum 0}
      tokens))))

(let [answer (parse-and-sum-muls "xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))")]
  (println "Part 1 (Example):" answer))
(let [answer (parse-and-sum-muls-with-conditions "xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))")]
  (println "Part 2 (Example):" answer))

(let [answer (parse-and-sum-muls (slurp "data/day03.txt"))]
  (println "Part 1:" answer))
(let [answer (parse-and-sum-muls-with-conditions (slurp "data/day03.txt"))]
  (println "Part 2:" answer))
 
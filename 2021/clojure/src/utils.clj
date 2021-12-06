(ns utils
  (:require [clojure.string :as str]))

(defn parse-integer [base xs]
  (Integer/parseInt (str/join "" xs) base))

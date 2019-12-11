package main

import (
	"bufio"
	"flag"
	"log"
	"os"
	"strings"
)

var inputFilename string

func init() {
	flag.StringVar(&inputFilename, "input", "input.txt", "Input file name")
}

func calculateLengths(connections map[string][]string, lengths map[string]int, d int, source string) {
	lengths[source] = d

	for _, target := range connections[source] {
		calculateLengths(connections, lengths, d+1, target)
	}
}

func part1(connections map[string][]string, lengths map[string]int) int {
	answer := 0
	for _, length := range lengths {
		answer += length
	}

	return answer
}

func getPath(connectionsReversed map[string]string, source, target string) []string {
	var path []string
	for this := source; this != target; this = connectionsReversed[this] {
		path = append([]string{this}, path...)
	}
	return path
}

func part2(connectionsReversed map[string]string, lengths map[string]int) int {
	pathA := getPath(connectionsReversed, "YOU", "COM")
	pathB := getPath(connectionsReversed, "SAN", "COM")

	var i int
	for i = 0; i < len(pathA) && i < len(pathB) && pathA[i] == pathB[i]; i++ {
	}
	i--

	return lengths["YOU"] + lengths["SAN"] - 2 - (lengths[pathA[i]] * 2)
}

func main() {
	var err error

	flag.Parse()

	f, err := os.Open(inputFilename)
	if err != nil {
		log.Fatal(err)
	}

	scanner := bufio.NewScanner(f)

	connections := make(map[string][]string)
	connectionsReversed := make(map[string]string)

	for scanner.Scan() {
		objs := strings.SplitN(scanner.Text(), ")", 2)
		if len(objs) != 2 {
			log.Panic("incorrect input file format")
		}
		connections[objs[0]] = append(connections[objs[0]], objs[1])
		connectionsReversed[objs[1]] = objs[0]
	}

	if err := scanner.Err(); err != nil {
		log.Panic(err)
	}

	lengths := make(map[string]int)
	calculateLengths(connections, lengths, 0, "COM")

	log.Println("Part 1:", part1(connections, lengths))
	log.Println("Part 2:", part2(connectionsReversed, lengths))
}

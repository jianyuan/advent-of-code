package main

import (
	"flag"
	"fmt"
	"io/ioutil"
	"log"
	"strings"
)

var inputFilename string

func init() {
	flag.StringVar(&inputFilename, "input", "input.txt", "Input file name")
}

func main() {
	var err error

	flag.Parse()

	inputData, err := ioutil.ReadFile(inputFilename)
	if err != nil {
		log.Fatal(err)
	}

	rawNumbers := strings.TrimSpace(string(inputData))
	numbers := make([]int, 0, len(rawNumbers))
	for _, rawNumber := range []rune(rawNumbers) {
		numbers = append(numbers, int(rawNumber-'0'))
	}

	w, h := 25, 6

	if len(numbers)%(w*h) != 0 {
		log.Panic("image data corrupted")
	}

	log.Println("Part 1:", part1(numbers, w, h))
	log.Println("Part 2:")
	part2(numbers, w, h)
}

func part1(numbers []int, w, h int) int {
	layers := len(numbers) / (w * h)
	var minZero int
	var answer int

	for i := 0; i < layers; i++ {
		layerNumbers := numbers[i*(w*h) : (i+1)*(w*h)]
		counter := make(map[int]int)

		fmt.Println(layerNumbers)

		for _, layerNumber := range layerNumbers {
			counter[layerNumber]++
		}

		if minZero == 0 || minZero > counter[0] {
			answer = counter[1] * counter[2]
			minZero = counter[0]
		}
	}

	return answer
}

func part2(numbers []int, w, h int) {
	layers := len(numbers) / (w * h)
	for i := 0; i < h; i++ {
		for j := 0; j < w; j++ {
			pixel := numbers[(i*w)+j]
			for k := 1; k < layers && pixel == 2; k++ {
				pixel = numbers[k*(w*h)+(i*w)+j]
			}
			if pixel == 0 {
				fmt.Print(" ")
			} else if pixel == 1 {
				fmt.Print("█")
			}
		}
		fmt.Println()
	}
}

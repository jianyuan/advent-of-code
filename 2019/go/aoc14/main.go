package main

import (
	"flag"
	"fmt"
	"io/ioutil"
	"log"
	"strings"

	"github.com/kr/pretty"
)

func ceilDiv(a, b int) int {
	c := a / b
	if a%b != 0 {
		c++
	}
	return c
}

type Chemical struct {
	Name     string
	Quantity int
}

type Reaction struct {
	Inputs []Chemical
	Output Chemical
}

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

	rawInput := strings.TrimSpace(string(inputData))
	rawInputLines := strings.Split(rawInput, "\n")

	reactions := make(map[string]Reaction)
	for _, rawInputLine := range rawInputLines {
		parts := strings.Split(rawInputLine, " => ")

		output := Chemical{}
		fmt.Sscanf(parts[1], "%d %s", &output.Quantity, &output.Name)

		inputs := []Chemical{}
		for _, part := range strings.Split(parts[0], ", ") {
			input := Chemical{}
			fmt.Sscanf(part, "%d %s", &input.Quantity, &input.Name)
			inputs = append(inputs, input)
		}

		reactions[output.Name] = Reaction{
			Inputs: inputs,
			Output: output,
		}
	}

	needs := make(map[string]Chemical)
	needs["FUEL"] = Chemical{Name: "FUEL", Quantity: 1}
	extras := make(map[string]int)
	raws := make(map[string]int)

	for len(needs) > 0 {
		pretty.Println()
		pretty.Println("===>")

		newNeeds := make(map[string]Chemical)
		for _, need := range needs {
			pretty.Println()
			pretty.Println("=>", need)

			reaction := reactions[need.Name]

			if len(reaction.Inputs) == 1 && reaction.Inputs[0].Name == "ORE" {
				raws[need.Name] += need.Quantity
			} else {
				need.Quantity -= extras[need.Name]
				extras[need.Name] = 0

				n := ceilDiv(need.Quantity, reaction.Output.Quantity)

				fmt.Println("need:", need, "x", n)

				for _, input := range reaction.Inputs {
					if newNeed, ok := newNeeds[input.Name]; ok {
						newNeeds[input.Name] = Chemical{
							Name:     input.Name,
							Quantity: newNeed.Quantity + input.Quantity*n,
						}
					} else {
						newNeeds[input.Name] = Chemical{
							Name:     input.Name,
							Quantity: input.Quantity * n,
						}
					}
				}

				extras[need.Name] += (n * reaction.Output.Quantity) - need.Quantity
			}
		}

		pretty.Println("prev:", needs)
		pretty.Println("next:", newNeeds)
		pretty.Println("extras:", extras)
		pretty.Println("raws:", raws)

		needs = newNeeds
	}

	oresNeeded := 0
	for name, quantity := range raws {
		reaction := reactions[name]
		n := ceilDiv(quantity, reaction.Output.Quantity)
		oresNeeded += n * reaction.Inputs[0].Quantity
	}

	log.Println("Ores needed:", oresNeeded)
}

func eql(a, b map[string]Chemical) bool {
	if len(a) != len(b) {
		return false
	}
	for k, v1 := range a {
		v2, ok := b[k]
		if !ok {
			return false
		}

		if v1 != v2 {
			return false
		}
	}
	return true
}

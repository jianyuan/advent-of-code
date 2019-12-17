package main

import (
	"flag"
	"io/ioutil"
	"log"
	"math"
	"regexp"
	"strconv"
	"strings"
)

type Point struct {
	X, Y, Z int
}

func (p Point) Energy() int {
	return int(math.Abs(float64(p.X)) + math.Abs(float64(p.Y)) + math.Abs(float64(p.Z)))
}

var (
	inputFilename string
	inputRegexp   = regexp.MustCompile(`<x=([\-\d]+), y=([\-\d]+), z=([\-\d]+)>`)
)

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
	rawSubmatches := inputRegexp.FindAllStringSubmatch(rawInput, -1)
	moons := make([]Point, 0, len(rawSubmatches))
	for _, rawSubmatch := range rawSubmatches {
		var p Point
		p.X, _ = strconv.Atoi(rawSubmatch[1])
		p.Y, _ = strconv.Atoi(rawSubmatch[2])
		p.Z, _ = strconv.Atoi(rawSubmatch[3])
		moons = append(moons, p)
	}

	simulationSteps := 1000
	velocities := make([]Point, len(moons))

	for step := 0; step < simulationSteps; step++ {
		// fmt.Println("step", step, moons, velocities)

		for i := 0; i < len(moons); i++ {
			for j := 0; j < len(moons); j++ {
				if i == j {
					continue
				}

				if moons[i].X < moons[j].X {
					velocities[i].X++
				} else if moons[i].X > moons[j].X {
					velocities[i].X--
				}

				if moons[i].Y < moons[j].Y {
					velocities[i].Y++
				} else if moons[i].Y > moons[j].Y {
					velocities[i].Y--
				}

				if moons[i].Z < moons[j].Z {
					velocities[i].Z++
				} else if moons[i].Z > moons[j].Z {
					velocities[i].Z--
				}
			}
		}

		for i := 0; i < len(moons); i++ {
			moons[i].X += velocities[i].X
			moons[i].Y += velocities[i].Y
			moons[i].Z += velocities[i].Z
		}
	}

	var totalEnergy int
	for i := 0; i < len(moons); i++ {
		totalEnergy += moons[i].Energy() * velocities[i].Energy()
	}

	log.Println("Part 1", totalEnergy)

}

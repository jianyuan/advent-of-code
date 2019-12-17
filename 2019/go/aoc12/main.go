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

	log.Println("Part 1", part1(moons))
	log.Println("Part 2", part2(moons))
}

func part1(moons []Point) int {
	simulationSteps := 1000
	copiedMoons := make([]Point, len(moons))
	copy(copiedMoons, moons)
	velocities := make([]Point, len(moons))

	for step := 0; step < simulationSteps; step++ {
		simulateOnce(copiedMoons, velocities)
	}

	var totalEnergy int
	for i := 0; i < len(copiedMoons); i++ {
		totalEnergy += copiedMoons[i].Energy() * velocities[i].Energy()
	}
	return totalEnergy
}

func GCD(a, b int) int {
	for b != 0 {
		t := b
		b = a % b
		a = t
	}
	return a
}

func LCM(a, b int) int {
	return a * b / GCD(a, b)
}

func part2(initialMoons []Point) int {
	initialVelocity := make([]Point, len(initialMoons))

	var steps int
	var cyclesX, cyclesY, cyclesZ int
	moons := make([]Point, len(initialMoons))
	copy(moons, initialMoons)
	velocities := make([]Point, len(initialMoons))

	for cyclesX == 0 || cyclesY == 0 || cyclesZ == 0 {
		simulateOnce(moons, velocities)

		steps++

		if cyclesX == 0 && pointsEqual(moons, initialMoons, velocities, initialVelocity, func(p Point) int { return p.X }) {
			cyclesX = steps
		}

		if cyclesY == 0 && pointsEqual(moons, initialMoons, velocities, initialVelocity, func(p Point) int { return p.Y }) {
			cyclesY = steps
		}

		if cyclesZ == 0 && pointsEqual(moons, initialMoons, velocities, initialVelocity, func(p Point) int { return p.Z }) {
			cyclesZ = steps
		}
	}

	return LCM(cyclesX, LCM(cyclesY, cyclesZ))
}

func pointsEqual(a, b, c, d []Point, f func(Point) int) bool {
	if len(a) != len(b) {
		return false
	}
	if len(c) != len(d) {
		return false
	}
	for i, v := range a {
		if f(v) != f(b[i]) {
			return false
		}
	}
	for i, v := range c {
		if f(v) != f(d[i]) {
			return false
		}
	}
	return true
}

func simulateOnce(moons []Point, velocities []Point) {
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

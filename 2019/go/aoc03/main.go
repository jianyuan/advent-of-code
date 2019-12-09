package main

import (
	"bytes"
	"log"
	"math"
	"os"
	"strconv"
	"strings"
)

type Direction int

func (d Direction) Apply(other Coordinate) Coordinate {
	switch d {
	case Up:
		other.Y++
	case Down:
		other.Y--
	case Left:
		other.X--
	case Right:
		other.X++
	}
	return other
}

const (
	Up Direction = iota
	Down
	Left
	Right
)

type Vector struct {
	Magnitude int
	Direction Direction
}

type Coordinate struct {
	X, Y int
}

func (c Coordinate) ManhattanDistance() int {
	return int(math.Abs(float64(c.X)) + math.Abs(float64(c.Y)))
}

func parseInstructions(rawWireDirectionLine string) []Vector {
	rawWireDirections := strings.Split(rawWireDirectionLine, ",")
	wireDirections := make([]Vector, 0, len(rawWireDirections))
	for _, rawWireDirection := range rawWireDirections {
		var direction Direction
		switch rawWireDirection[0] {
		case 'U':
			direction = Up
		case 'D':
			direction = Down
		case 'L':
			direction = Left
		case 'R':
			direction = Right
		default:
			log.Panic("Unknown direction:", rawWireDirection[0])
		}

		magnitude, err := strconv.ParseInt(rawWireDirection[1:], 10, 64)
		if err != nil {
			log.Panic(err)
		}

		wireDirections = append(wireDirections, Vector{
			Magnitude: int(magnitude),
			Direction: direction,
		})
	}

	return wireDirections
}

func part1(wireVectorLines [][]Vector) int {
	visited := make(map[Coordinate]struct{})
	var minCoordinate Coordinate
	for i, wireVectors := range wireVectorLines {
		var coordinate Coordinate
		for _, wireVector := range wireVectors {
			for j := 0; j < wireVector.Magnitude; j++ {
				coordinate = wireVector.Direction.Apply(coordinate)
				if i == 0 {
					// first run
					visited[coordinate] = struct{}{}
				} else {
					if _, ok := visited[coordinate]; ok {
						if (minCoordinate.X == 0 && minCoordinate.Y == 0) || minCoordinate.ManhattanDistance() > coordinate.ManhattanDistance() {
							minCoordinate = coordinate
						}
					}
				}
			}
		}
	}
	return minCoordinate.ManhattanDistance()
}

func part2(wireVectorLines [][]Vector) int {
	wire1CoordinateSteps := make(map[Coordinate]int)
	wire2Visited := make(map[Coordinate]struct{})
	var minSteps int

	// Wire 1
	{
		var steps int
		var coordinate Coordinate

		for _, wireVector := range wireVectorLines[0] {
			for i := 0; i < wireVector.Magnitude; i++ {
				coordinate = wireVector.Direction.Apply(coordinate)
				steps++
				wire1CoordinateSteps[coordinate] = steps
			}
		}
	}

	// Wire 2
	{
		var steps int
		var coordinate Coordinate

		for _, wireVector := range wireVectorLines[1] {
			for i := 0; i < wireVector.Magnitude; i++ {
				coordinate = wireVector.Direction.Apply(coordinate)
				steps++
				if wire1Steps, ok := wire1CoordinateSteps[coordinate]; ok {
					if _, visited := wire2Visited[coordinate]; !visited {
						if thisSteps := wire1Steps + steps; minSteps == 0 || minSteps > thisSteps {
							minSteps = thisSteps
						}
						wire2Visited[coordinate] = struct{}{}
					}
				}
			}
		}
	}

	return minSteps
}

func main() {
	var b bytes.Buffer
	_, err := b.ReadFrom(os.Stdin)
	if err != nil {
		log.Fatal(err)
	}

	rawInput := strings.TrimSpace(b.String())
	rawWireVectorLines := strings.SplitN(rawInput, "\n", 2)
	if len(rawWireVectorLines) != 2 {
		log.Panic("Expecting only 2 lines of input")
	}
	wireVectorLines := make([][]Vector, 0, 2)
	for _, rawWireVectorLines := range rawWireVectorLines {
		wireVectorLines = append(wireVectorLines, parseInstructions(rawWireVectorLines))
	}

	log.Println("Part 1: ", part1(wireVectorLines))
	log.Println("Part 2: ", part2(wireVectorLines))
}

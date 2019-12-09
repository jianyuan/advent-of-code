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

	log.Println("Part 1: ", minCoordinate.ManhattanDistance())
}

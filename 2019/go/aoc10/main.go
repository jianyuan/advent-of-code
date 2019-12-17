package main

import (
	"flag"
	"io/ioutil"
	"log"
	"math"
	"sort"
	"strings"
)

type Tile rune

const (
	Empty    Tile = '.'
	Asteroid      = '#'
)

type Point struct {
	X, Y float64
}

func (p Point) Sub(other Point) Point {
	return Point{p.X - other.X, p.Y - other.Y}
}

func (p Point) Hypot() float64 {
	return math.Hypot(p.X, p.Y)
}

func (p Point) Normalised() Point {
	l := p.Hypot()
	return Point{p.X / l, p.Y / l}
}

func (p Point) DotProduct(other Point) float64 {
	return p.X*other.X + p.Y*other.Y
}

var (
	DirectionUp = Point{0, -1}
)

type AngleDistance struct {
	Point    Point
	Origin   Point
	Angle    float64
	Distance float64
}

func angleAndDistance(point Point, origin Point, direction Point) AngleDistance {
	vector := point.Sub(origin)
	l := vector.Hypot()

	if l == 0 {
		// No angle
		return AngleDistance{Point: point, Origin: origin, Angle: -math.Pi, Distance: l}
	}

	normalisedVector := vector.Normalised()
	dotProduct := normalisedVector.X*direction.X + normalisedVector.Y*direction.Y
	diffProduct := direction.Y*normalisedVector.X - direction.X*normalisedVector.Y
	angle := math.Atan2(diffProduct, dotProduct)

	if angle > 0 {
		return AngleDistance{Point: point, Origin: origin, Angle: angle - 2*math.Pi, Distance: l}
	}

	return AngleDistance{Point: point, Origin: origin, Angle: angle, Distance: l}
}

func iterAsteroidsTile(m [][]Tile, f func(Point)) {
	for i := 0; i < len(m); i++ {
		for j := 0; j < len(m[i]); j++ {
			if m[i][j] != Asteroid {
				continue
			}

			f(Point{float64(j), float64(i)})
		}
	}
}

func countVisible(m [][]Tile, origin Point) int {
	unique := make(map[float64]struct{})

	iterAsteroidsTile(m, func(point Point) {
		if point == origin {
			return
		}

		angleDistance := angleAndDistance(point, origin, DirectionUp)
		unique[angleDistance.Angle] = struct{}{}
	})

	return len(unique)
}

func part1(input [][]Tile) int {
	var maxVisible int

	iterAsteroidsTile(input, func(point Point) {
		visible := countVisible(input, point)

		if visible > maxVisible {
			maxVisible = visible
		}
	})

	return maxVisible
}

func part2(input [][]Tile) int {
	var angleDistances []AngleDistance
	var origin Point
	var maxVisible int

	iterAsteroidsTile(input, func(point Point) {
		visible := countVisible(input, point)

		if visible > maxVisible {
			origin = point
			maxVisible = visible
		}
	})

	iterAsteroidsTile(input, func(point Point) {
		if point == origin {
			return
		}

		angleDistance := angleAndDistance(point, origin, DirectionUp)
		angleDistances = append(angleDistances, angleDistance)
	})

	sort.Slice(angleDistances, func(i, j int) bool {
		if angleDistances[i].Angle > angleDistances[j].Angle {
			return true
		}
		if angleDistances[i].Angle < angleDistances[j].Angle {
			return false
		}
		return angleDistances[i].Distance < angleDistances[j].Distance
	})

	var i int
	pointsSeen := make(map[AngleDistance]struct{})
	for len(angleDistances) != len(pointsSeen) {
		anglesSeen := make(map[float64]struct{})

		for _, angleDistance := range angleDistances {
			if _, seen := pointsSeen[angleDistance]; seen {
				continue
			}

			if _, seen := anglesSeen[angleDistance.Angle]; seen {
				continue
			}

			i++
			if i == 200 {
				return int(angleDistance.Point.X*100 + angleDistance.Point.Y)
			}

			pointsSeen[angleDistance] = struct{}{}
			anglesSeen[angleDistance.Angle] = struct{}{}
		}
	}

	return 0
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

	input := make([][]Tile, 0, len(rawInputLines))
	for _, rawInputLine := range rawInputLines {
		input = append(input, []Tile(rawInputLine))
	}

	log.Println("Part 1:", part1(input))
	log.Println("Part 2:", part2(input))
}

package main

import (
	"flag"
	"fmt"
	"io/ioutil"
	"log"
	"math"
	"strconv"
	"strings"
	"sync"
)

type InstructionMode func(cpu *CPU, value int, write bool) int

func PositionMode(cpu *CPU, value int, write bool) int {
	if write {
		return value
	}
	return cpu.Memory[value]
}

func ImmediateMode(cpu *CPU, value int, write bool) int {
	return value
}

func RelativeMode(cpu *CPU, value int, write bool) int {
	addr := cpu.relativeBase + value
	if write {
		return addr
	}
	return cpu.Memory[addr]
}

var (
	instructionModes = map[int]InstructionMode{
		0: PositionMode,
		1: ImmediateMode,
		2: RelativeMode,
	}
)

func getDigit(n, digit int) int {
	return (n / int(math.Pow10(digit))) % 10
}

type InputReader interface {
	Read() int
}

type OutputWriter interface {
	Write(int)
}

type CPU struct {
	id           int
	pc           int
	relativeBase int
	Memory       []int

	InputReader  InputReader
	OutputWriter OutputWriter
}

func (cpu *CPU) getValue(offset int, write bool) int {
	positionCodes := cpu.Memory[cpu.pc] / 100
	instructionMode := instructionModes[getDigit(positionCodes, offset)]
	return instructionMode(cpu, cpu.Memory[cpu.pc+1+offset], write)
}

func (cpu *CPU) RunUntilFinish() {
	for cpu.pc < len(cpu.Memory) {
		fullOpcode := cpu.Memory[cpu.pc]
		opcode := fullOpcode % 100

		// fmt.Println("==> opcode", fullOpcode)
		// fmt.Println("==> pc before", cpu.pc)
		// fmt.Println("==> before", cpu.Memory)

		switch opcode {
		case 1: // add
			a := cpu.getValue(0, false)
			b := cpu.getValue(1, false)
			w := cpu.getValue(2, true)
			cpu.Memory[w] = a + b
			cpu.pc += 4
		case 2: // multiply
			a := cpu.getValue(0, false)
			b := cpu.getValue(1, false)
			w := cpu.getValue(2, true)
			cpu.Memory[w] = a * b
			cpu.pc += 4
		case 3: // store
			w := cpu.getValue(0, true)
			value := cpu.InputReader.Read()
			// log.Println(cpu.id, "Input:", value)
			cpu.Memory[w] = value
			cpu.pc += 2
		case 4: // print
			a := cpu.getValue(0, false)
			// log.Println(cpu.id, "Output:", a)
			cpu.OutputWriter.Write(a)
			cpu.pc += 2
		case 5: // jump-if-true
			a := cpu.getValue(0, false)
			b := cpu.getValue(1, false)
			if a != 0 {
				cpu.pc = b
			} else {
				cpu.pc += 3
			}
		case 6: // jump-if-false
			a := cpu.getValue(0, false)
			b := cpu.getValue(1, false)
			if a == 0 {
				cpu.pc = b
			} else {
				cpu.pc += 3
			}
		case 7: // less than
			a := cpu.getValue(0, false)
			b := cpu.getValue(1, false)
			w := cpu.getValue(2, true)

			if a < b {
				cpu.Memory[w] = 1
			} else {
				cpu.Memory[w] = 0
			}
			cpu.pc += 4
		case 8: // equals
			a := cpu.getValue(0, false)
			b := cpu.getValue(1, false)
			w := cpu.getValue(2, true)

			if a == b {
				cpu.Memory[w] = 1
			} else {
				cpu.Memory[w] = 0
			}
			cpu.pc += 4
		case 9: // adjust relative base
			a := cpu.getValue(0, false)
			cpu.relativeBase += a
			cpu.pc += 2
		case 99: // stop
			return
		default:
			log.Fatalln("Opcode not implemented:", opcode, "PC:", cpu.pc)
		}

		// fmt.Println("<== pc after", cpu.pc)
		// fmt.Println("<== after", cpu.Memory)
	}
}

func runCPU(id int, memory []int, inputReader InputReader, outputWriter OutputWriter) *CPU {
	newMemory := make([]int, 10000)
	copy(newMemory, memory)
	cpu := &CPU{
		id:           id,
		Memory:       newMemory,
		InputReader:  inputReader,
		OutputWriter: outputWriter,
	}
	cpu.RunUntilFinish()
	return cpu
}

type SliceInputReader struct {
	Data    []int
	pointer int
}

func (s *SliceInputReader) Read() int {
	value := s.Data[s.pointer]
	s.pointer++
	return value
}

type SliceOutputWriter struct {
	Data []int
}

func (s *SliceOutputWriter) Write(value int) {
	s.Data = append(s.Data, value)
}

type ChanInputReader struct {
	done chan bool
	Ch   chan int
}

func (c *ChanInputReader) Read() int {
	return <-c.Ch
}

type ChanOutputWriter struct {
	Ch chan int
}

func (c *ChanOutputWriter) Write(value int) {
	c.Ch <- value
}

type Point struct {
	X, Y int
}

func (p Point) Add(other Point) Point {
	return Point{p.X + other.X, p.Y + other.Y}
}

var (
	DirectionUp       = Point{0, -1}
	DirectionDown     = Point{0, 1}
	DirectionLeft     = Point{-1, 0}
	DirectionRight    = Point{1, 0}
	DirectionTurnings = map[Point]map[int]Point{
		DirectionUp: {
			0: DirectionLeft,
			1: DirectionRight,
		},
		DirectionDown: {
			0: DirectionRight,
			1: DirectionLeft,
		},
		DirectionLeft: {
			0: DirectionDown,
			1: DirectionUp,
		},
		DirectionRight: {
			0: DirectionUp,
			1: DirectionDown,
		},
	}
)

var inputFilename string

func init() {
	flag.StringVar(&inputFilename, "input", "input.txt", "Input file name")
}

func part1(memory []int) int {
	reader := &ChanInputReader{Ch: make(chan int, 1)}
	writer := &ChanOutputWriter{Ch: make(chan int, 1)}
	quit := make(chan struct{})
	answer := make(chan map[Point]int)

	go func() {
		runCPU(0, memory, reader, writer)
		close(quit)
	}()

	go func() {
		painted := make(map[Point]int)
		pos := Point{}
		direction := DirectionUp

		for {

			select {
			default:
				reader.Ch <- painted[pos]
				color := <-writer.Ch
				nextDirection := <-writer.Ch

				painted[pos] = color

				direction = DirectionTurnings[direction][nextDirection]
				pos = pos.Add(direction)

			case <-quit:
				answer <- painted
				return
			}
		}
	}()

	return len(<-answer)
}

func part2(memory []int) {
	reader := &ChanInputReader{Ch: make(chan int, 1)}
	writer := &ChanOutputWriter{Ch: make(chan int, 1)}
	quit := make(chan struct{})

	go func() {
		runCPU(0, memory, reader, writer)
		close(quit)
	}()

	var wg sync.WaitGroup
	wg.Add(1)

	go func() {
		defer wg.Done()

		painted := make(map[Point]int)
		painted[Point{}] = 1
		pos := Point{}
		direction := DirectionUp

		minX, maxX := 0, 0
		minY, maxY := 0, 0

		for {

			select {
			default:
				reader.Ch <- painted[pos]
				color := <-writer.Ch
				nextDirection := <-writer.Ch

				painted[pos] = color

				direction = DirectionTurnings[direction][nextDirection]
				pos = pos.Add(direction)

				if pos.X > maxX {
					maxX = pos.X
				} else if pos.X < minX {
					minX = pos.X
				}

				if pos.Y > maxY {
					maxY = pos.Y
				} else if pos.Y < minY {
					minY = pos.Y
				}

			case <-quit:
				for i := minY; i <= maxY; i++ {
					for j := minX; j <= maxX; j++ {
						if painted[Point{j, i}] == 0 {
							fmt.Print(" ")
						} else if painted[Point{j, i}] == 1 {
							fmt.Print("█")
						}
					}
					fmt.Println()
				}
				return
			}
		}
	}()

	wg.Wait()
}

func main() {
	var err error

	flag.Parse()

	inputData, err := ioutil.ReadFile(inputFilename)
	if err != nil {
		log.Fatal(err)
	}

	rawInput := strings.TrimSpace(string(inputData))
	rawInputNumbers := strings.Split(rawInput, ",")

	memory := make([]int, 0, len(rawInputNumbers))
	for _, rawInputNumber := range rawInputNumbers {
		rawInt, err := strconv.ParseInt(rawInputNumber, 10, 64)
		if err != nil {
			log.Fatal(err)
		}
		memory = append(memory, int(rawInt))
	}

	log.Println("Part 1:", part1(memory))
	log.Println("Part 2:")
	part2(memory)
}

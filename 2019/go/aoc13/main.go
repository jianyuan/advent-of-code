package main

import (
	"bufio"
	"flag"
	"fmt"
	"io"
	"io/ioutil"
	"log"
	"math"
	"os"
	"strconv"
	"strings"

	tm "github.com/buger/goterm"
	tomb "gopkg.in/tomb.v2"
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
	newMemory := make([]int, 1000000)
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

type IOInputReader struct {
	r io.Reader
}

func (s *IOInputReader) Read() int {
	scanner := bufio.NewScanner(os.Stdin)
	for {
		fmt.Println("Input:")
		scanner.Scan()
		v, err := strconv.Atoi(scanner.Text())
		if err != nil {
			log.Fatal(err)
		}
		return v
	}
}

type SliceOutputWriter struct {
	Data []int
}

func (s *SliceOutputWriter) Write(value int) {
	s.Data = append(s.Data, value)
}

type ChanInputReader struct {
	done   chan bool
	NextCh chan struct{}
	Ch     chan int
}

func NewChanInputReader() *ChanInputReader {
	r := &ChanInputReader{
		NextCh: make(chan struct{}),
		Ch:     make(chan int),
	}
	return r
}

func (c *ChanInputReader) Read() int {
	c.NextCh <- struct{}{}
	return <-c.Ch
}

type ChanOutputWriter struct {
	Ch chan int
}

func NewChanOutputWriter() *ChanOutputWriter {
	w := &ChanOutputWriter{
		Ch: make(chan int),
	}
	return w
}

func (c *ChanOutputWriter) Write(value int) {
	c.Ch <- value
}

type LogOutputWriter struct{}

func (LogOutputWriter) Write(value int) {
	log.Println(value)
}

var inputFilename string

func init() {
	flag.StringVar(&inputFilename, "input", "input.txt", "Input file name")
}

func part1(memory []int) int {
	reader := &SliceInputReader{}
	writer := &SliceOutputWriter{}
	runCPU(0, memory, reader, writer)

	var n int

	for i := 0; i < len(writer.Data); i += 3 {
		if Tiles[writer.Data[i+2]] == TileBlock {
			n++
		}
	}

	return n
}

func part2(input []int) {
	memory := make([]int, len(input))
	copy(memory, input)

	// play for free
	memory[0] = 2

	reader := NewChanInputReader()
	writer := NewChanOutputWriter()
	var t tomb.Tomb

	ballCh := make(chan int)
	paddleCh := make(chan int)
	outputFinish := make(chan struct{})

	// Output
	t.Go(func() error {
		var ballX, paddleX int

		for {
			select {
			case <-t.Dying():
				return nil

			case ballX = <-ballCh:

			case paddleX = <-paddleCh:

			case <-reader.NextCh:

			loop1:
				for {
					select {
					case ballX = <-ballCh:
					case paddleX = <-paddleCh:
					case <-outputFinish:
						break loop1
					}
				}

				var v int

				if paddleX > ballX {
					v = -1
				} else if paddleX < ballX {
					v = 1
				} else {
					v = 0
				}

				reader.Ch <- v
			}
		}
	})

	// Input
	t.Go(func() error {
		var score int
		var maxX, maxY int
		tiles := make(map[Point]Tile)

		for {
			select {
			case <-t.Dying():
				return nil

			case x := <-writer.Ch:
				y, id := <-writer.Ch, <-writer.Ch
				p := Point{x, y}

				if p.X == -1 && p.Y == 0 {
					score = id
				} else {
					if p.X > maxX {
						maxX = p.X
					}
					if p.Y > maxY {
						maxY = p.Y
					}

					t := Tiles[id]
					tiles[p] = t

					switch t {
					case TilePaddle:
						paddleCh <- p.X
					case TileBall:
						ballCh <- p.X
					}
				}

				tm.Clear()
				tm.MoveCursor(1, 1)
				tm.Println("Score:", score)
				for i := 0; i < maxY; i++ {
					for j := 0; j < maxX; j++ {
						tm.Print(tiles[Point{j, i}].Symbol)
					}
					tm.Println()
				}
				tm.Flush()

			case outputFinish <- struct{}{}:

			}
		}
	})

	runCPU(0, memory, reader, writer)

	t.Kill(nil)

	t.Wait()
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

	// log.Println("Part 1:", part1(memory))
	log.Println("Part 2:")
	part2(memory)
}

type Tile struct {
	Symbol string
}

var (
	TileEmpty  = Tile{" "}
	TileWall   = Tile{" "}
	TileBlock  = Tile{"•"}
	TilePaddle = Tile{"•"}
	TileBall   = Tile{tm.Color(tm.Bold("•"), tm.RED)}
	Tiles      = map[int]Tile{
		0: TileEmpty,
		1: TileWall,
		2: TileBlock,
		3: TilePaddle,
		4: TileBall,
	}
)

type Point struct {
	X, Y int
}

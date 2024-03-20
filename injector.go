package main

import (
	"io/ioutil"
	"log"
	"os"
)

func mergePrograms(targetBinaryPath, injectorBinaryPath string) error {
	// Read the target binary
	targetBinary, err := ioutil.ReadFile(targetBinaryPath)
	if err != nil {
		return err
	}

	// Read the injector binary
	injectorBinary, err := ioutil.ReadFile(injectorBinaryPath)
	if err != nil {
		return err
	}

	// Determine the insertion point in the target binary
	// For example, you could insert the injector binary at the beginning of the target binary
	insertionPoint := 0

	// Insert the injector binary into the target binary
	modifiedBinary := append(targetBinary[:insertionPoint], injectorBinary...)
	modifiedBinary = append(modifiedBinary, targetBinary[insertionPoint:]...)

	// Write the modified target binary back to disk
	err = ioutil.WriteFile(targetBinaryPath, modifiedBinary, 0644)
	if err != nil {
		return err
	}

	log.Printf("Injected %s into %s\n", injectorBinaryPath, targetBinaryPath)
	return nil
}

func main() {
	if len(os.Args) != 3 {
		log.Fatalf("Usage: %s <target> <injector>", os.Args[0])
	}

	target := os.Args[1]
	injector := os.Args[2]

	err := mergePrograms(target, injector)
	if err != nil {
		log.Fatal(err)
	}
}

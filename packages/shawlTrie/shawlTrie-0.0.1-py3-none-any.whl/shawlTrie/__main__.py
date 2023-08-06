from .cli import trieClass


def main():
	trie = trieClass()

	msg = input('Enter task (add, search, autocomplete, delete, display): ')

	if msg == 'add':
		text = input('Type word to add: ')
		trie.add(text)
		trie.save()
		print('Word has been added successfully!')

	elif msg == 'search':
		text = input('Type word to search: ')
		print(trie.search(text)[0])

	elif msg == 'autocomplete':
		text = input('Type prefix to autocomplete: ')
		print(trie.autocomplete(text))

	elif msg == 'delete':
		text = input('Type word to delete: ')
		trie.delete(text)
		trie.save()

	elif msg == 'display':
		trie.prefix=''
		trie.display(trie.root)

	else:
		print('Invalid task. Try Again')


if __name__ == '__main__':
	main()
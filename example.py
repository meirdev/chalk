from chalk import chalk

# Combine styled and normal strings
print(chalk.blue("Hello") + " World" + chalk.red("!"))

# Compose multiple styles using the chainable API
print(chalk.blue.bg_red.bold("Hello world!"))

# Pass in multiple arguments
print(chalk.blue("Hello", "World!", "Foo", "bar", "biz", "baz"))

# Nest styles
print(chalk.red("Hello", chalk.underline.bg_blue("world") + "!"))

# Nest styles of the same type even (color, underline, background)
print(chalk.green(
	"I am a green line " +
	chalk.blue.underline.bold("with a blue substring") +
	" that becomes green again!"
))

# f-string
print(f"""
CPU: {chalk.red("90%")}
RAM: {chalk.green("40%")}
DISK: {chalk.yellow("70%")}
""")

# Use RGB colors in terminal emulators that support it.
print(chalk.rgb(123, 45, 67).underline("Underlined reddish color"))
print(chalk.hex("#DEADED").bold("Bold gray!"))

# Easily define your own themes
error = chalk.bold.red
warning = chalk.hex('#FFA500')

print(error('Error!'))
print(warning('Warning!'))

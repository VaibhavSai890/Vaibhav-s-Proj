import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.awt.event.MouseAdapter;
import java.awt.event.MouseEvent;
import javax.swing.*;
import javax.swing.text.*;
import java.util.Random;

// Define a Character class as the base class for both Player and Enemy
class Character {
    String name;
    int health;
    int attackPower;

    // Constructor
    public Character(String name, int health, int attackPower) {
        this.name = name;
        this.health = health;
        this.attackPower = attackPower;
    }

    // Method to attack another character
    public void attack(Character target, JTextPane logArea) {
        int damage = this.attackPower;
        if (target instanceof Player && ((Player) target).isDefenseActive()) {
            damage /= 2;
        }
        ((TurnBasedRPGSwing) SwingUtilities.getWindowAncestor(logArea)).appendToPane(logArea, name + " attacks " + target.name + " for " + damage + " damage!\n", Color.YELLOW);
        target.health -= damage;
        ((TurnBasedRPGSwing) SwingUtilities.getWindowAncestor(logArea)).appendToPane(logArea, target.name + "'s health: " + target.health + "\n", Color.YELLOW);
    }
}

// Player class inheriting from Character
class Player extends Character {
    private boolean defenseActive;

    // Constructor
    public Player(String name, int health, int attackPower) {
        super(name, health, attackPower);
        this.defenseActive = false;
    }

    // Method to defend, reducing damage by half
    public void defend(JTextPane logArea) {
        ((TurnBasedRPGSwing) SwingUtilities.getWindowAncestor(logArea)).appendToPane(logArea, name + " raises a shield!\n", Color.YELLOW);
        this.defenseActive = true;
    }

    public boolean isDefenseActive() {
        return defenseActive;
    }

    public void resetDefense() {
        this.defenseActive = false;
    }

    // Method to use an item (example representation)
    public void useItem(String itemName, JTextPane logArea) {
        ((TurnBasedRPGSwing) SwingUtilities.getWindowAncestor(logArea)).appendToPane(logArea, name + " uses " + itemName + "!\n", Color.YELLOW);
    }
}

// Enemy class inheriting from Character
class Enemy extends Character {
    int minAttackPower;
    int maxAttackPower;

    // Constructor
    public Enemy(String name, int health, int minAttackPower, int maxAttackPower) {
        super(name, health, (minAttackPower + maxAttackPower) / 2); // Average attack power for display
        this.minAttackPower = minAttackPower;
        this.maxAttackPower = maxAttackPower;
    }

    // Method to generate random attack power within a range
    public int generateRandomAttackPower() {
        Random random = new Random();
        return random.nextInt((maxAttackPower - minAttackPower) + 1) + minAttackPower;
    }

    // Override the attack method to use random attack power
    @Override
    public void attack(Character target, JTextPane logArea) {
        int randomAttackPower = generateRandomAttackPower();
        int damage = randomAttackPower;
        if (target instanceof Player && ((Player) target).isDefenseActive()) {
            damage /= 2; // Halve the damage if the hero defends
        }
        ((TurnBasedRPGSwing) SwingUtilities.getWindowAncestor(logArea)).appendToPane(logArea, name + " attacks " + target.name + " for " + damage + " damage!\n", Color.YELLOW);
        target.health -= damage;
        ((TurnBasedRPGSwing) SwingUtilities.getWindowAncestor(logArea)).appendToPane(logArea, target.name + "'s health: " + target.health + "\n", Color.YELLOW);
    }
}

// Main class to run the game
public class TurnBasedRPGSwing extends JFrame {
    private Player player;
    private Enemy[] enemies;
    private int currentEnemyIndex;
    private JTextPane logArea;
    private JLabel playerHealthLabel;
    private JLabel enemyHealthLabel;
    private JLabel actionImageLabel;
    private JButton attackButton;
    private JButton defendButton;
    private JButton useItemButton;

    public TurnBasedRPGSwing() {
        // Initialize player and enemies
        player = new Player("Hero", 100, 10);
        enemies = new Enemy[]{
                new Enemy("Monster", 50, 5, 10),
                new Enemy("Goblin", 60, 10, 13),
                new Enemy("Dragon", 80, 13, 15)
        };
        currentEnemyIndex = 0;

        // Set up the GUI
        setTitle("Turn-Based RPG Game");
        setSize(600, 600);
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        setLocationRelativeTo(null);
        setLayout(new BorderLayout());
        getContentPane().setBackground(Color.BLACK); // Set background color to black

        logArea = new JTextPane();
        logArea.setEditable(false);
        logArea.setBackground(Color.BLACK); // Set background color to black
        Font mainTextFont = new Font("Arial", Font.PLAIN, 18);
        logArea.setFont(mainTextFont);
        add(new JScrollPane(logArea), BorderLayout.CENTER);

        JPanel controlPanel = new JPanel();
        controlPanel.setLayout(new GridLayout(3, 1));
        controlPanel.setBackground(Color.BLACK); // Set background color to black

        JPanel playerPanel = new JPanel();
        playerPanel.setBackground(Color.BLACK); // Set background color to black
        playerHealthLabel = new JLabel("Player Health: " + player.health);
        playerHealthLabel.setForeground(Color.YELLOW); // Set text color to yellow
        playerHealthLabel.setFont(new Font("Arial", Font.BOLD, 24)); // Set font size and bold
        playerPanel.add(playerHealthLabel);
        controlPanel.add(playerPanel);

        JPanel enemyPanel = new JPanel();
        enemyPanel.setBackground(Color.BLACK); // Set background color to black
        enemyHealthLabel = new JLabel("Enemy Health: " + enemies[currentEnemyIndex].health);
        enemyHealthLabel.setForeground(Color.YELLOW); // Set text color to yellow
        enemyHealthLabel.setFont(new Font("Arial", Font.BOLD, 24)); // Set font size and bold
        enemyPanel.add(enemyHealthLabel);
        controlPanel.add(enemyPanel);

        actionImageLabel = new JLabel();
        controlPanel.add(actionImageLabel);

        add(controlPanel, BorderLayout.NORTH);

        JPanel actionPanel = new JPanel();
        actionPanel.setBackground(Color.BLACK); // Set background color to black

        // Create buttons with visual feedback
        attackButton = createButton("Attack");
        defendButton = createButton("Defend");
        useItemButton = createButton("Use Item");

        actionPanel.add(attackButton);
        actionPanel.add(defendButton);
        actionPanel.add(useItemButton);

        add(actionPanel, BorderLayout.SOUTH);

        // Display the welcome message
        appendToPane(logArea, "Welcome to the Turn-Based RPG Game!\n", Color.YELLOW);
        appendToPane(logArea, "You are " + player.name + " with " + player.health + " health and " + player.attackPower + " attack power.\n", Color.YELLOW);
        appendToPane(logArea, "Prepare to face multiple enemies!\n\n", Color.YELLOW);

        // Display the first enemy
        appendToPane(logArea, "An enemy " + enemies[currentEnemyIndex].name + " appears with " + enemies[currentEnemyIndex].health + " health and attack power range " + enemies[currentEnemyIndex].minAttackPower + "-" + enemies[currentEnemyIndex].maxAttackPower + "!\n", Color.YELLOW);
    }

    // Method to create buttons with visual feedback
    private JButton createButton(String text) {
        JButton button = new JButton(text);
        button.setBackground(Color.YELLOW); // Set initial background color
        button.setForeground(Color.BLACK);
        button.setFont(new Font("Arial", Font.BOLD, 18));
        button.setPreferredSize(new Dimension(120, 40));

        // Add mouse listener for visual feedback
        button.addMouseListener(new MouseAdapter() {
            @Override
            public void mouseEntered(MouseEvent e) {
                button.setBackground(Color.ORANGE); // Change color on hover
            }

            @Override
            public void mouseExited(MouseEvent e) {
                button.setBackground(Color.YELLOW); // Revert color on exit
            }

            @Override
            public void mousePressed(MouseEvent e) {
                button.setBackground(Color.RED); // Change color when pressed
            }

            @Override
            public void mouseReleased(MouseEvent e) {
                button.setBackground(Color.ORANGE); // Change color back on release
            }
        });

        // Add action listener for button functionality
        button.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                if (text.equals("Attack")) {
                    playerAttack();
                } else if (text.equals("Defend")) {
                    playerDefend();
                } else if (text.equals("Use Item")) {
                    useItem();
                }
            }
        });

        return button;
    }

    private void playerAttack() {
        actionImageLabel.setIcon(new ImageIcon("attack.png"));
        player.attack(enemies[currentEnemyIndex], logArea);
        updateHealthLabels();
        if (enemies[currentEnemyIndex].health <= 0) {
            appendToPane(logArea, "You defeated the " + enemies[currentEnemyIndex].name + "!\n", Color.YELLOW);
            currentEnemyIndex++;
            if (currentEnemyIndex < enemies.length) {
                appendToPane(logArea, "An enemy " + enemies[currentEnemyIndex].name + " appears with " + enemies[currentEnemyIndex].health + " health and attack power range " + enemies[currentEnemyIndex].minAttackPower + "-" + enemies[currentEnemyIndex].maxAttackPower + "!\n", Color.YELLOW);
            } else {
                appendToPane(logArea, "Congratulations! You have defeated all the enemies!\n", Color.YELLOW);
                disableButtons();
            }
        } else {
            enemyAttack();
        }
    }

    private void playerDefend() {
        actionImageLabel.setIcon(new ImageIcon("defend.png"));
        player.defend(logArea);
        enemyAttack();
    }

    private void useItem() {
        Object[] options = {"Attack Potion", "Health Potion"};
        String item = (String) JOptionPane.showInputDialog(this, "Choose an item to use:", "Use Item", JOptionPane.PLAIN_MESSAGE, null, options, "Attack Potion");
        if (item != null) {
            actionImageLabel.setIcon(new ImageIcon("use_item.png"));
            player.useItem(item, logArea);
            if (item.equals("Attack Potion")) {
                player.attackPower += 5; // Increase attack power by 5
                appendToPane(logArea, "Attack power increased to " + player.attackPower + "\n", Color.YELLOW);
            } else if (item.equals("Health Potion")) {
                player.health += 20; // Increase health by 20
                appendToPane(logArea, "Health restored to " + player.health + "\n", Color.YELLOW);
            }
            updateHealthLabels();
            enemyAttack();
        }
    }

    private void enemyAttack() {
        appendToPane(logArea, "\n<span style='color: cyan; font-size: 20px;'>=== Enemy's Turn ===</span>\n", Color.CYAN);
        enemies[currentEnemyIndex].attack(player, logArea);
        player.resetDefense();
        updateHealthLabels();
        if (player.health <= 0) {
            appendToPane(logArea, "Game Over! You were defeated by the " + enemies[currentEnemyIndex].name + ".\n", Color.YELLOW);
            disableButtons();
        }
    }

    private void updateHealthLabels() {
        playerHealthLabel.setText("Player Health: " + player.health);
        if (currentEnemyIndex < enemies.length) {
            enemyHealthLabel.setText("Enemy Health: " + enemies[currentEnemyIndex].health);
        } else {
            enemyHealthLabel.setText("No Enemies Left");
        }
    }

    private void disableButtons() {
        attackButton.setEnabled(false);
        defendButton.setEnabled(false);
        useItemButton.setEnabled(false);
    }

    // Method to append colored text to JTextPane
    public void appendToPane(JTextPane tp, String msg, Color c) {
        StyledDocument doc = tp.getStyledDocument();
        Style style = tp.addStyle("Color Style", null);
        StyleConstants.setForeground(style, c);
        try {
            doc.insertString(doc.getLength(), msg, style);
        } catch (BadLocationException e) {
            e.printStackTrace();
        }
    }

    public static void main(String[] args) {
        SwingUtilities.invokeLater(new Runnable() {
            @Override
            public void run() {
                new TurnBasedRPGSwing().setVisible(true);
            }
        });
    }
}

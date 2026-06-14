from flask import Flask, render_template, request, jsonify
import random
import time

app = Flask(__name__)

# --- Game Assets ---
gifts = ['sticker', 'lollipop', 'cookie', 'blankie']
anger_items = ['drink', 'cup of tea', 'stress ball']
hehe_responses = [
    'ERROR: System crashing...Thank you for the extra tip of $149!',
    'Security has been called. Please stay exactly where you are.',
    'Fine! We are keeping all cookies from you! Hmph.',
    'A hex has been placed upon your credit score.']


@app.route('/')
def home():
    # Serves the main website page
    return render_template('new_index.html')


@app.route('/process_mood', methods=['POST'])
def process_mood():
    data = request.json
    greet = data.get('mood', '').strip().lower()

    choice = random.choice(gifts)
    angry_item = random.choice(anger_items)

    # Determine price and text based on mood
    if greet in ["happy", "good", "fine"]:
        text = "Glad to hear that! Please proceed to checkout to pay."
        price = 20
        prompt = f"Please pay ${price}. Pay now? (yes/no):"
    elif greet == "sad":
        if random.choice([True, False]):
            text = f"Sorry about that! Have a {choice}!"
            price = 25
        else:
            text = "Sorry about that, but your overwhelming emotional damage is costing us three tissues.\nThat will be a $5 emotional cleanup fee."
            price = 30
        prompt = f"Please pay ${price}. Pay now? (yes/no):"
    elif greet in ["angry", "mad", "miffed", "annoyed"]:
        text = f"Oof! Why don't you take a {angry_item} to calm down?."
        price = 27
        prompt = f"Please pay ${price}. Pay now? (yes/no):"
    elif greet in ["tired", "bored"]:
        text = "You should take a nap! Sleep is free, but our advice is not."
        price = 23
        prompt = f"Please pay ${price}. Pay now? (yes/no):"
    else:
        text = f"We don't recognize that emotion. Have a {choice}!"
        price = 29
        prompt = f"Please pay ${price}. Pay now? (yes/no):"

    return jsonify({'text': text, 'prompt': prompt, 'price': price})


@app.route('/process_payment', methods=['POST'])
def process_payment():
    data = request.json
    pay_input = data.get('payment', '').strip()
    mood = data.get('mood', '').strip().lower()
    price = data.get('price', 20)

    # 20% chance of random event
    event_text = ""
    if random.random() < 1.0:
        event = random.choice([
            "A raccoon broke into the cash register! Please pay $55 for our damages",
            "A robber broke in. We are now charging everyone an extra 5 dollars."
        ])
        event_text = f"\n\n🚨🚨🚨: {event}"
        if "discount" in event:
            price -= 5

    # Check if payment is successful
    payment_successful = pay_input.lower() in ["yes", "okay", "fine", "ok", "alright"]

    if payment_successful:
        final_text = f"Successfully charged ${price}!\n\nThank you! Come again!"
    else:
        final_text = f"Transaction Declined.\n\n{random.choice(hehe_responses)}"

    # return jsonify({'event_text': event_text, 'final_text': final_text})
    return jsonify({'final_text': final_text, 'event_text': event_text})


if __name__ == '__main__':
    app.run(debug=True)
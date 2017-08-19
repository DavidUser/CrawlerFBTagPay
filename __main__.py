import crawler

def main():
    """Main function
    """

    merchants = [
        crawler.Merchant('276973842707396')
    ]

    for merchant in merchants:
        merchant.update_all_payments()
        print "Merchant: " + merchant.id
        merchant.print_payments()

if __name__ == "__main__":
    main()

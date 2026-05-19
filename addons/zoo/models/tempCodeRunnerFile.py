    def test_create(self):
        self.env['demo.student'].create({
            'name': 'White rare tiger',
            'dob': '2024-12-11',
            'gender': 'female',
            'feed_time': '2024-12-20 13:39:25',
            'age': 0
        })
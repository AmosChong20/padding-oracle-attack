const mongoose = require('mongoose');

const userSchema = new mongoose.Schema({
    username: {
        type: String,
        required: true,
    },
    password: {
        type: String,
        required: true,
    },
    accountBalance: {
        type: Number,
        default: 350000,
    },
})

const User = mongoose.model('User', userSchema);

module.exports = User;
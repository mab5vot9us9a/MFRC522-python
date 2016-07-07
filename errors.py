#!/usr/bin/env python3
# coding=utf-8
# Copyright © 2016 Maurice Fahn All Rights Reserved.


class TextTooLongException(Exception):
    """Exception for when the text is too long."""

    def __init__(self, message="Text is too long."):
        super(TextTooLongException, self).__init__(message)


class AuthenticationException(Exception):
    """Exception for when the authentication failed."""

    def __init__(self, message="Authentication failed."):
        super(AuthenticationException, self).__init__(message)


class InvalidValueException(Exception):
    """Exception for when the passed value is invalid"""
    pass

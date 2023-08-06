# Copyright 2021 by LivingLogic AG, Bayreuth/Germany
# Copyright 2021 by Walter Dörwald
#
# All Rights Reserved
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.


from pygments import token, style


class LivingLogicLightStyle(style.Style):
	"""
	The 'LivingLogic' style, light version
	"""

	# overall background color (``None`` means transparent)
	background_color = '#00000003'

	# highlight background color
	highlight_color = '#0f02'

	# line number font color
	line_number_color = '#6f6f6f'

	# line number background color
	line_number_background_color = 'transparent'

	# special line number font color (``:emphasize-lines`` in Sphinx code blocks)
	line_number_special_color = '#5d5d5d'

	# special line number background color (``:emphasize-lines`` in Sphinx code blocks)
	line_number_special_background_color = 'transparent'

	styles = {
		token.Token:                '#191919',
		token.Generic.Output:       '#6f6f6f',
		token.Generic.Prompt:       '#a5a5a5',
		token.Generic.Error:        '#ff1c1c',
		token.Generic.Traceback:    '#ff1c1c',
		token.Comment:              '#4c4c4c',
		token.Number:               '#e700e6',
		token.String:               '#0a0',
		token.String.Doc:           '#396339',
		token.String.Interpol:      '#060',
		token.String.Delimiter:     '#060',
		token.String.Escape:        '#060',
		token.String.Affix:         '#060',
		token.Token.Literal.Date:   '#00797a',
		token.Token.Literal.Color:  '#00797a',
		token.Keyword:              '#0051f6',
		token.Keyword.Reserved:     '#a92b00',
		token.Operator:             '#0051f6',
		token.Operator.Word:        '#0051f6',
		token.Keyword.Constant:     '#774600',
		token.Name:                 '#191919',
		token.Name.Class:           '#191919 bold',
		token.Name.Function:        '#191919 bold',
		token.Name.Namespace:       '#191919',
		token.Name.Builtin.Pseudo:  '#102b62',
		token.Name.Variable.Magic:  '#102b62',
		token.Name.Function.Magic:  '#102b62',
		token.Name.Tag:             '#993d00',
		token.Name.Attribute:       '#cf9670',
		token.Name.Entity:          '#e700e6',
		token.Comment.Preproc:      '#006061',
		token.Token.Prompt:         '#006a00',
		token.Token.PromptNum:      '#005400',
		token.Token.OutPrompt:      '#ff1c1c',
		token.Token.OutPromptNum:   '#cc1616',
	}


class LivingLogicDarkStyle(style.Style):
	"""
	The 'LivingLogic' style, dark version
	"""

	# overall background color (``None`` means transparent)
	background_color = '#ffffff03'

	# highlight background color
	highlight_color = '#030'

	# line number font color
	line_number_color = '#8e8e8e'

	# line number background color
	line_number_background_color = 'transparent'

	# special line number font color (``:emphasize-lines`` in Sphinx code blocks)
	line_number_special_color = '#a0a0a0'

	# special line number background color (``:emphasize-lines`` in Sphinx code blocks)
	line_number_special_background_color = 'transparent'

	styles = {
		token.Token:                '#e5e5e5',
		token.Generic.Output:       '#a0a0a0',
		token.Generic.Prompt:       '#7c7c7c',
		token.Generic.Error:        '#ff9d9d',
		token.Generic.Traceback:    '#ff9d9d',
		token.Comment:              '#b2b2b2',
		token.Number:               '#eb9beb',
		token.String:               '#a4c240',
		token.String.Doc:           '#aeb695',
		token.String.Interpol:      '#d1e09f',
		token.String.Delimiter:     '#d1e09f',
		token.String.Escape:        '#d1e09f',
		token.String.Affix:         '#d1e09f',
		token.Token.Literal.Date:   '#51cccc',
		token.Token.Literal.Color:  '#51cccc',
		token.Keyword:              '#7fbce2',
		token.Keyword.Reserved:     '#dbaa89',
		token.Operator:             '#7fbce2',
		token.Operator.Word:        '#7fbce2',
		token.Keyword.Constant:     '#ffa929',
		token.Name:                 '#e5e5e5',
		token.Name.Class:           '#e5e5e5 bold',
		token.Name.Function:        '#e5e5e5 bold',
		token.Name.Namespace:       '#e5e5e5',
		token.Name.Builtin.Pseudo:  '#c3d7e4',
		token.Name.Variable.Magic:  '#c3d7e4',
		token.Name.Function.Magic:  '#c3d7e4',
		token.Name.Tag:             '#ffa366',
		token.Name.Attribute:       '#dcb397',
		token.Name.Entity:          '#eb9beb',
		token.Comment.Preproc:      '#00e2e2',
		token.Token.Prompt:         '#00f900',
		token.Token.PromptNum:      '#7ffc7f',
		token.Token.OutPrompt:      '#ff9d9d',
		token.Token.OutPromptNum:   '#ffcece',
	}

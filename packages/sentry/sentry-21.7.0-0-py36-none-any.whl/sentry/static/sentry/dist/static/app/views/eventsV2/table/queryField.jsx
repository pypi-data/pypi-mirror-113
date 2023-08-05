Object.defineProperty(exports, "__esModule", { value: true });
exports.QueryField = void 0;
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var react_select_1 = require("react-select");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var cloneDeep_1 = tslib_1.__importDefault(require("lodash/cloneDeep"));
var selectControl_1 = tslib_1.__importDefault(require("app/components/forms/selectControl"));
var tag_1 = tslib_1.__importDefault(require("app/components/tag"));
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var input_1 = tslib_1.__importDefault(require("app/views/settings/components/forms/controls/input"));
var arithmeticInput_1 = tslib_1.__importDefault(require("./arithmeticInput"));
var types_1 = require("./types");
var QueryField = /** @class */ (function (_super) {
    tslib_1.__extends(QueryField, _super);
    function QueryField() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.FieldSelectComponents = {
            Option: function (_a) {
                var label = _a.label, data = _a.data, props = tslib_1.__rest(_a, ["label", "data"]);
                return (<react_select_1.components.Option label={label} data={data} {...props}>
        <span data-test-id="label">{label}</span>
        {_this.renderTag(data.value.kind)}
      </react_select_1.components.Option>);
            },
            SingleValue: function (_a) {
                var data = _a.data, props = tslib_1.__rest(_a, ["data"]);
                return (<react_select_1.components.SingleValue data={data} {...props}>
        <span data-test-id="label">{data.label}</span>
        {_this.renderTag(data.value.kind)}
      </react_select_1.components.SingleValue>);
            },
        };
        _this.FieldSelectStyles = {
            singleValue: function (provided) {
                var custom = {
                    display: 'flex',
                    justifyContent: 'space-between',
                    alignItems: 'center',
                    width: 'calc(100% - 10px)',
                };
                return tslib_1.__assign(tslib_1.__assign({}, provided), custom);
            },
            option: function (provided) {
                var custom = {
                    display: 'flex',
                    justifyContent: 'space-between',
                    alignItems: 'center',
                    width: '100%',
                };
                return tslib_1.__assign(tslib_1.__assign({}, provided), custom);
            },
        };
        _this.handleFieldChange = function (selected) {
            if (!selected) {
                return;
            }
            var value = selected.value;
            var current = _this.props.fieldValue;
            var fieldValue = cloneDeep_1.default(_this.props.fieldValue);
            switch (value.kind) {
                case types_1.FieldValueKind.TAG:
                case types_1.FieldValueKind.MEASUREMENT:
                case types_1.FieldValueKind.BREAKDOWN:
                case types_1.FieldValueKind.FIELD:
                    fieldValue = { kind: 'field', field: value.meta.name };
                    break;
                case types_1.FieldValueKind.FUNCTION:
                    if (current.kind === 'field') {
                        fieldValue = {
                            kind: 'function',
                            function: [value.meta.name, '', undefined, undefined],
                        };
                    }
                    else if (current.kind === 'function') {
                        fieldValue = {
                            kind: 'function',
                            function: [
                                value.meta.name,
                                current.function[1],
                                current.function[2],
                                current.function[3],
                            ],
                        };
                    }
                    break;
                default:
                    throw new Error('Invalid field type found in column picker');
            }
            if (value.kind === types_1.FieldValueKind.FUNCTION) {
                value.meta.parameters.forEach(function (param, i) {
                    if (fieldValue.kind !== 'function') {
                        return;
                    }
                    if (param.kind === 'column') {
                        var field = _this.getFieldOrTagOrMeasurementValue(fieldValue.function[i + 1]);
                        if (field === null) {
                            fieldValue.function[i + 1] = param.defaultValue || '';
                        }
                        else if ((field.kind === types_1.FieldValueKind.FIELD ||
                            field.kind === types_1.FieldValueKind.TAG ||
                            field.kind === types_1.FieldValueKind.MEASUREMENT ||
                            field.kind === types_1.FieldValueKind.BREAKDOWN) &&
                            validateColumnTypes(param.columnTypes, field)) {
                            // New function accepts current field.
                            fieldValue.function[i + 1] = field.meta.name;
                        }
                        else {
                            // field does not fit within new function requirements, use the default.
                            fieldValue.function[i + 1] = param.defaultValue || '';
                            fieldValue.function[i + 2] = undefined;
                        }
                    }
                    else {
                        fieldValue.function[i + 1] = param.defaultValue || '';
                    }
                });
                if (fieldValue.kind === 'function') {
                    if (value.meta.parameters.length === 0) {
                        fieldValue.function = [fieldValue.function[0], '', undefined, undefined];
                    }
                    else if (value.meta.parameters.length === 1) {
                        fieldValue.function[2] = undefined;
                    }
                }
            }
            _this.triggerChange(fieldValue);
        };
        _this.handleEquationChange = function (value) {
            var newColumn = cloneDeep_1.default(_this.props.fieldValue);
            if (newColumn.kind === types_1.FieldValueKind.EQUATION) {
                newColumn.field = value;
            }
            _this.triggerChange(newColumn);
        };
        _this.handleFieldParameterChange = function (_a) {
            var value = _a.value;
            var newColumn = cloneDeep_1.default(_this.props.fieldValue);
            if (newColumn.kind === 'function') {
                newColumn.function[1] = value.meta.name;
            }
            _this.triggerChange(newColumn);
        };
        _this.handleDropdownParameterChange = function (index) {
            return function (value) {
                var newColumn = cloneDeep_1.default(_this.props.fieldValue);
                if (newColumn.kind === 'function') {
                    newColumn.function[index] = value.value;
                }
                _this.triggerChange(newColumn);
            };
        };
        _this.handleScalarParameterChange = function (index) {
            return function (value) {
                var newColumn = cloneDeep_1.default(_this.props.fieldValue);
                if (newColumn.kind === 'function') {
                    newColumn.function[index] = value;
                }
                _this.triggerChange(newColumn);
            };
        };
        return _this;
    }
    QueryField.prototype.triggerChange = function (fieldValue) {
        this.props.onChange(fieldValue);
    };
    QueryField.prototype.getFieldOrTagOrMeasurementValue = function (name) {
        var fieldOptions = this.props.fieldOptions;
        if (name === undefined) {
            return null;
        }
        var fieldName = "field:" + name;
        if (fieldOptions[fieldName]) {
            return fieldOptions[fieldName].value;
        }
        var measurementName = "measurement:" + name;
        if (fieldOptions[measurementName]) {
            return fieldOptions[measurementName].value;
        }
        var spanOperationBreakdownName = "span_op_breakdown:" + name;
        if (fieldOptions[spanOperationBreakdownName]) {
            return fieldOptions[spanOperationBreakdownName].value;
        }
        var tagName = name.indexOf('tags[') === 0
            ? "tag:" + name.replace(/tags\[(.*?)\]/, '$1')
            : "tag:" + name;
        if (fieldOptions[tagName]) {
            return fieldOptions[tagName].value;
        }
        // Likely a tag that was deleted but left behind in a saved query
        // Cook up a tag option so select control works.
        if (name.length > 0) {
            return {
                kind: types_1.FieldValueKind.TAG,
                meta: {
                    name: name,
                    dataType: 'string',
                    unknown: true,
                },
            };
        }
        return null;
    };
    QueryField.prototype.getFieldData = function () {
        var _this = this;
        var field = null;
        var fieldValue = this.props.fieldValue;
        var fieldOptions = this.props.fieldOptions;
        if (fieldValue.kind === 'function') {
            var funcName = "function:" + fieldValue.function[0];
            if (fieldOptions[funcName] !== undefined) {
                field = fieldOptions[funcName].value;
            }
        }
        if (fieldValue.kind === 'field') {
            field = this.getFieldOrTagOrMeasurementValue(fieldValue.field);
            fieldOptions = this.appendFieldIfUnknown(fieldOptions, field);
        }
        var parameterDescriptions = [];
        // Generate options and values for each parameter.
        if (field &&
            field.kind === types_1.FieldValueKind.FUNCTION &&
            field.meta.parameters.length > 0 &&
            fieldValue.kind === types_1.FieldValueKind.FUNCTION) {
            parameterDescriptions = field.meta.parameters.map(function (param, index) {
                if (param.kind === 'column') {
                    var fieldParameter = _this.getFieldOrTagOrMeasurementValue(fieldValue.function[1]);
                    fieldOptions = _this.appendFieldIfUnknown(fieldOptions, fieldParameter);
                    return {
                        kind: 'column',
                        value: fieldParameter,
                        required: param.required,
                        options: Object.values(fieldOptions).filter(function (_a) {
                            var value = _a.value;
                            return (value.kind === types_1.FieldValueKind.FIELD ||
                                value.kind === types_1.FieldValueKind.TAG ||
                                value.kind === types_1.FieldValueKind.MEASUREMENT ||
                                value.kind === types_1.FieldValueKind.BREAKDOWN) &&
                                validateColumnTypes(param.columnTypes, value);
                        }),
                    };
                }
                else if (param.kind === 'dropdown') {
                    return {
                        kind: 'dropdown',
                        options: param.options,
                        dataType: param.dataType,
                        required: param.required,
                        value: (fieldValue.kind === 'function' && fieldValue.function[index + 1]) ||
                            param.defaultValue ||
                            '',
                    };
                }
                return {
                    kind: 'value',
                    value: (fieldValue.kind === 'function' && fieldValue.function[index + 1]) ||
                        param.defaultValue ||
                        '',
                    dataType: param.dataType,
                    required: param.required,
                    placeholder: param.placeholder,
                };
            });
        }
        return { field: field, fieldOptions: fieldOptions, parameterDescriptions: parameterDescriptions };
    };
    QueryField.prototype.appendFieldIfUnknown = function (fieldOptions, field) {
        if (!field) {
            return fieldOptions;
        }
        if (field && field.kind === types_1.FieldValueKind.TAG && field.meta.unknown) {
            // Clone the options so we don't mutate other rows.
            fieldOptions = Object.assign({}, fieldOptions);
            fieldOptions[field.meta.name] = { label: field.meta.name, value: field };
        }
        return fieldOptions;
    };
    QueryField.prototype.renderParameterInputs = function (parameters) {
        var _this = this;
        var _a = this.props, disabled = _a.disabled, inFieldLabels = _a.inFieldLabels, filterAggregateParameters = _a.filterAggregateParameters, hideParameterSelector = _a.hideParameterSelector;
        var inputs = parameters.map(function (descriptor, index) {
            if (descriptor.kind === 'column' && descriptor.options.length > 0) {
                if (hideParameterSelector) {
                    return null;
                }
                var aggregateParameters = filterAggregateParameters
                    ? descriptor.options.filter(filterAggregateParameters)
                    : descriptor.options;
                return (<selectControl_1.default key="select" name="parameter" placeholder={locale_1.t('Select value')} options={aggregateParameters} value={descriptor.value} required={descriptor.required} onChange={_this.handleFieldParameterChange} inFieldLabel={inFieldLabels ? locale_1.t('Parameter: ') : undefined} disabled={disabled} styles={!inFieldLabels ? _this.FieldSelectStyles : undefined} components={_this.FieldSelectComponents}/>);
            }
            if (descriptor.kind === 'value') {
                var inputProps = {
                    required: descriptor.required,
                    value: descriptor.value,
                    onUpdate: _this.handleScalarParameterChange(index + 1),
                    placeholder: descriptor.placeholder,
                    disabled: disabled,
                };
                switch (descriptor.dataType) {
                    case 'number':
                        return (<BufferedInput name="refinement" key="parameter:number" type="text" inputMode="numeric" pattern="[0-9]*(\.[0-9]*)?" {...inputProps}/>);
                    case 'integer':
                        return (<BufferedInput name="refinement" key="parameter:integer" type="text" inputMode="numeric" pattern="[0-9]*" {...inputProps}/>);
                    default:
                        return (<BufferedInput name="refinement" key="parameter:text" type="text" {...inputProps}/>);
                }
            }
            if (descriptor.kind === 'dropdown') {
                return (<selectControl_1.default name="dropdown" placeholder={locale_1.t('Select value')} options={descriptor.options} value={descriptor.value} required={descriptor.required} onChange={_this.handleDropdownParameterChange(index + 1)} inFieldLabel={inFieldLabels ? locale_1.t('Parameter: ') : undefined} disabled={disabled}/>);
            }
            throw new Error("Unknown parameter type encountered for " + _this.props.fieldValue);
        });
        // Add enough disabled inputs to fill the grid up.
        // We always have 1 input.
        var gridColumns = this.props.gridColumns;
        var requiredInputs = (gridColumns !== null && gridColumns !== void 0 ? gridColumns : inputs.length + 1) - inputs.length - 1;
        if (gridColumns !== undefined && requiredInputs > 0) {
            for (var i = 0; i < requiredInputs; i++) {
                inputs.push(<BlankSpace key={i}/>);
            }
        }
        return inputs;
    };
    QueryField.prototype.renderTag = function (kind) {
        var shouldRenderTag = this.props.shouldRenderTag;
        if (shouldRenderTag === false) {
            return null;
        }
        var text, tagType;
        switch (kind) {
            case types_1.FieldValueKind.FUNCTION:
                text = 'f(x)';
                tagType = 'success';
                break;
            case types_1.FieldValueKind.MEASUREMENT:
                text = 'measure';
                tagType = 'info';
                break;
            case types_1.FieldValueKind.BREAKDOWN:
                text = 'breakdown';
                tagType = 'error';
                break;
            case types_1.FieldValueKind.TAG:
                text = kind;
                tagType = 'warning';
                break;
            case types_1.FieldValueKind.FIELD:
                text = kind;
                tagType = 'highlight';
                break;
            default:
                text = kind;
        }
        return <tag_1.default type={tagType}>{text}</tag_1.default>;
    };
    QueryField.prototype.render = function () {
        var _a = this.props, className = _a.className, takeFocus = _a.takeFocus, filterPrimaryOptions = _a.filterPrimaryOptions, fieldValue = _a.fieldValue, inFieldLabels = _a.inFieldLabels, disabled = _a.disabled, hidePrimarySelector = _a.hidePrimarySelector, gridColumns = _a.gridColumns, otherColumns = _a.otherColumns;
        var _b = this.getFieldData(), field = _b.field, fieldOptions = _b.fieldOptions, parameterDescriptions = _b.parameterDescriptions;
        var allFieldOptions = filterPrimaryOptions
            ? Object.values(fieldOptions).filter(filterPrimaryOptions)
            : Object.values(fieldOptions);
        var selectProps = {
            name: 'field',
            options: Object.values(allFieldOptions),
            placeholder: locale_1.t('(Required)'),
            value: field,
            onChange: this.handleFieldChange,
            inFieldLabel: inFieldLabels ? locale_1.t('Function: ') : undefined,
            disabled: disabled,
        };
        if (takeFocus && field === null) {
            selectProps.autoFocus = true;
        }
        var parameters = this.renderParameterInputs(parameterDescriptions);
        if (fieldValue.kind === types_1.FieldValueKind.EQUATION) {
            return (<Container className={className} gridColumns={1} tripleLayout={false}>
          <arithmeticInput_1.default name="arithmetic" key="parameter:text" type="text" required value={fieldValue.field} onUpdate={this.handleEquationChange} options={otherColumns}/>
        </Container>);
        }
        // if there's more than 2 parameters, set gridColumns to 2 so they go onto the next line instead
        var containerColumns = parameters.length > 2 ? 2 : gridColumns ? gridColumns : parameters.length + 1;
        return (<Container className={className} gridColumns={containerColumns} tripleLayout={gridColumns === 3 && parameters.length > 2}>
        {!hidePrimarySelector && (<selectControl_1.default {...selectProps} styles={!inFieldLabels ? this.FieldSelectStyles : undefined} components={this.FieldSelectComponents}/>)}
        {parameters}
      </Container>);
    };
    return QueryField;
}(React.Component));
exports.QueryField = QueryField;
function validateColumnTypes(columnTypes, input) {
    if (typeof columnTypes === 'function') {
        return columnTypes({ name: input.meta.name, dataType: input.meta.dataType });
    }
    return columnTypes.includes(input.meta.dataType);
}
var Container = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  display: grid;\n  ", "\n  grid-gap: ", ";\n  align-items: center;\n\n  flex-grow: 1;\n"], ["\n  display: grid;\n  ", "\n  grid-gap: ", ";\n  align-items: center;\n\n  flex-grow: 1;\n"])), function (p) {
    return p.tripleLayout
        ? "grid-template-columns: 1fr 2fr;"
        : "grid-template-columns: repeat(" + p.gridColumns + ", 1fr);";
}, space_1.default(1));
/**
 * Because controlled inputs fire onChange on every key stroke,
 * we can't update the QueryField that often as it would re-render
 * the input elements causing focus to be lost.
 *
 * Using a buffered input lets us throttle rendering and enforce data
 * constraints better.
 */
var BufferedInput = /** @class */ (function (_super) {
    tslib_1.__extends(BufferedInput, _super);
    function BufferedInput(props) {
        var _this = _super.call(this, props) || this;
        _this.state = {
            value: _this.props.value,
        };
        _this.handleBlur = function () {
            if (_this.isValid) {
                _this.props.onUpdate(_this.state.value);
            }
            else {
                _this.setState({ value: _this.props.value });
            }
        };
        _this.handleChange = function (event) {
            if (_this.isValid) {
                _this.setState({ value: event.target.value });
            }
        };
        _this.input = React.createRef();
        return _this;
    }
    Object.defineProperty(BufferedInput.prototype, "isValid", {
        get: function () {
            if (!this.input.current) {
                return true;
            }
            return this.input.current.validity.valid;
        },
        enumerable: false,
        configurable: true
    });
    BufferedInput.prototype.render = function () {
        var _a = this.props, _ = _a.onUpdate, props = tslib_1.__rest(_a, ["onUpdate"]);
        return (<StyledInput {...props} ref={this.input} className="form-control" value={this.state.value} onChange={this.handleChange} onBlur={this.handleBlur}/>);
    };
    return BufferedInput;
}(React.Component));
// Set a min-width to allow shrinkage in grid.
var StyledInput = styled_1.default(input_1.default)(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  /* Match the height of the select boxes */\n  height: 41px;\n  min-width: 50px;\n"], ["\n  /* Match the height of the select boxes */\n  height: 41px;\n  min-width: 50px;\n"])));
var BlankSpace = styled_1.default('div')(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  /* Match the height of the select boxes */\n  height: 41px;\n  min-width: 50px;\n  background: ", ";\n  border-radius: ", ";\n  display: flex;\n  align-items: center;\n  justify-content: center;\n\n  &:after {\n    font-size: ", ";\n    content: '", "';\n    color: ", ";\n  }\n"], ["\n  /* Match the height of the select boxes */\n  height: 41px;\n  min-width: 50px;\n  background: ", ";\n  border-radius: ", ";\n  display: flex;\n  align-items: center;\n  justify-content: center;\n\n  &:after {\n    font-size: ", ";\n    content: '", "';\n    color: ", ";\n  }\n"])), function (p) { return p.theme.backgroundSecondary; }, function (p) { return p.theme.borderRadius; }, function (p) { return p.theme.fontSizeMedium; }, locale_1.t('No parameter'), function (p) { return p.theme.gray300; });
var templateObject_1, templateObject_2, templateObject_3;
//# sourceMappingURL=queryField.jsx.map
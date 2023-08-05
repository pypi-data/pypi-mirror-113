Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var isEqual_1 = tslib_1.__importDefault(require("lodash/isEqual"));
var omit_1 = tslib_1.__importDefault(require("lodash/omit"));
var indicator_1 = require("app/actionCreators/indicator");
var locale_1 = require("app/locale");
var submitRules_1 = tslib_1.__importDefault(require("../submitRules"));
var types_1 = require("../types");
var utils_1 = require("../utils");
var form_1 = tslib_1.__importDefault(require("./form"));
var handleError_1 = tslib_1.__importStar(require("./handleError"));
var modal_1 = tslib_1.__importDefault(require("./modal"));
var utils_2 = require("./utils");
var ModalManager = /** @class */ (function (_super) {
    tslib_1.__extends(ModalManager, _super);
    function ModalManager() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = _this.getDefaultState();
        _this.handleChange = function (field, value) {
            var _a;
            var values = tslib_1.__assign(tslib_1.__assign({}, _this.state.values), (_a = {}, _a[field] = value, _a));
            if (values.type !== types_1.RuleType.PATTERN && values.pattern) {
                values.pattern = '';
            }
            if (values.method !== types_1.MethodType.REPLACE && values.placeholder) {
                values.placeholder = '';
            }
            _this.setState(function (prevState) { return ({
                values: values,
                requiredValues: _this.getRequiredValues(values),
                errors: omit_1.default(prevState.errors, field),
            }); });
        };
        _this.handleSave = function () { return tslib_1.__awaiter(_this, void 0, void 0, function () {
            var _a, endpoint, api, onSubmitSuccess, closeModal, onGetNewRules, newRules, data, error_1;
            return tslib_1.__generator(this, function (_b) {
                switch (_b.label) {
                    case 0:
                        _a = this.props, endpoint = _a.endpoint, api = _a.api, onSubmitSuccess = _a.onSubmitSuccess, closeModal = _a.closeModal, onGetNewRules = _a.onGetNewRules;
                        newRules = onGetNewRules(this.state.values);
                        _b.label = 1;
                    case 1:
                        _b.trys.push([1, 3, , 4]);
                        return [4 /*yield*/, submitRules_1.default(api, endpoint, newRules)];
                    case 2:
                        data = _b.sent();
                        onSubmitSuccess(data);
                        closeModal();
                        return [3 /*break*/, 4];
                    case 3:
                        error_1 = _b.sent();
                        this.convertRequestError(handleError_1.default(error_1));
                        return [3 /*break*/, 4];
                    case 4: return [2 /*return*/];
                }
            });
        }); };
        _this.handleValidate = function (field) {
            return function () {
                var isFieldValueEmpty = !_this.state.values[field].trim();
                var fieldErrorAlreadyExist = _this.state.errors[field];
                if (isFieldValueEmpty && fieldErrorAlreadyExist) {
                    return;
                }
                if (isFieldValueEmpty && !fieldErrorAlreadyExist) {
                    _this.setState(function (prevState) {
                        var _a;
                        return ({
                            errors: tslib_1.__assign(tslib_1.__assign({}, prevState.errors), (_a = {}, _a[field] = locale_1.t('Field Required'), _a)),
                        });
                    });
                    return;
                }
                if (!isFieldValueEmpty && fieldErrorAlreadyExist) {
                    _this.clearError(field);
                }
            };
        };
        _this.handleUpdateEventId = function (eventId) {
            if (eventId === _this.state.eventId.value) {
                return;
            }
            _this.setState({
                eventId: { value: eventId, status: types_1.EventIdStatus.UNDEFINED },
            });
        };
        return _this;
    }
    ModalManager.prototype.componentDidMount = function () {
        this.handleValidateForm();
    };
    ModalManager.prototype.componentDidUpdate = function (_prevProps, prevState) {
        if (!isEqual_1.default(prevState.values, this.state.values)) {
            this.handleValidateForm();
        }
        if (prevState.eventId.value !== this.state.eventId.value) {
            this.loadSourceSuggestions();
        }
        if (prevState.eventId.status !== this.state.eventId.status) {
            utils_2.saveToSourceGroupData(this.state.eventId, this.state.sourceSuggestions);
        }
    };
    ModalManager.prototype.getDefaultState = function () {
        var _a = utils_2.fetchSourceGroupData(), eventId = _a.eventId, sourceSuggestions = _a.sourceSuggestions;
        var values = this.getInitialValues();
        return {
            values: values,
            requiredValues: this.getRequiredValues(values),
            errors: {},
            isFormValid: false,
            eventId: {
                value: eventId,
                status: !eventId ? types_1.EventIdStatus.UNDEFINED : types_1.EventIdStatus.LOADED,
            },
            sourceSuggestions: sourceSuggestions,
        };
    };
    ModalManager.prototype.getInitialValues = function () {
        var _a, _b, _c, _d, _e;
        var initialState = this.props.initialState;
        return {
            type: (_a = initialState === null || initialState === void 0 ? void 0 : initialState.type) !== null && _a !== void 0 ? _a : types_1.RuleType.CREDITCARD,
            method: (_b = initialState === null || initialState === void 0 ? void 0 : initialState.method) !== null && _b !== void 0 ? _b : types_1.MethodType.MASK,
            source: (_c = initialState === null || initialState === void 0 ? void 0 : initialState.source) !== null && _c !== void 0 ? _c : '',
            placeholder: (_d = initialState === null || initialState === void 0 ? void 0 : initialState.placeholder) !== null && _d !== void 0 ? _d : '',
            pattern: (_e = initialState === null || initialState === void 0 ? void 0 : initialState.pattern) !== null && _e !== void 0 ? _e : '',
        };
    };
    ModalManager.prototype.getRequiredValues = function (values) {
        var type = values.type;
        var requiredValues = ['type', 'method', 'source'];
        if (type === types_1.RuleType.PATTERN) {
            requiredValues.push('pattern');
        }
        return requiredValues;
    };
    ModalManager.prototype.clearError = function (field) {
        this.setState(function (prevState) { return ({
            errors: omit_1.default(prevState.errors, field),
        }); });
    };
    ModalManager.prototype.loadSourceSuggestions = function () {
        return tslib_1.__awaiter(this, void 0, void 0, function () {
            var _a, orgSlug, projectId, api, eventId, query, rawSuggestions, sourceSuggestions_1, _b;
            return tslib_1.__generator(this, function (_c) {
                switch (_c.label) {
                    case 0:
                        _a = this.props, orgSlug = _a.orgSlug, projectId = _a.projectId, api = _a.api;
                        eventId = this.state.eventId;
                        if (!eventId.value) {
                            this.setState(function (prevState) { return ({
                                sourceSuggestions: utils_1.valueSuggestions,
                                eventId: tslib_1.__assign(tslib_1.__assign({}, prevState.eventId), { status: types_1.EventIdStatus.UNDEFINED }),
                            }); });
                            return [2 /*return*/];
                        }
                        this.setState(function (prevState) { return ({
                            sourceSuggestions: utils_1.valueSuggestions,
                            eventId: tslib_1.__assign(tslib_1.__assign({}, prevState.eventId), { status: types_1.EventIdStatus.LOADING }),
                        }); });
                        _c.label = 1;
                    case 1:
                        _c.trys.push([1, 3, , 4]);
                        query = { eventId: eventId.value };
                        if (projectId) {
                            query.projectId = projectId;
                        }
                        return [4 /*yield*/, api.requestPromise("/organizations/" + orgSlug + "/data-scrubbing-selector-suggestions/", { query: query })];
                    case 2:
                        rawSuggestions = _c.sent();
                        sourceSuggestions_1 = rawSuggestions.suggestions;
                        if (sourceSuggestions_1 && sourceSuggestions_1.length > 0) {
                            this.setState(function (prevState) { return ({
                                sourceSuggestions: sourceSuggestions_1,
                                eventId: tslib_1.__assign(tslib_1.__assign({}, prevState.eventId), { status: types_1.EventIdStatus.LOADED }),
                            }); });
                            return [2 /*return*/];
                        }
                        this.setState(function (prevState) { return ({
                            sourceSuggestions: utils_1.valueSuggestions,
                            eventId: tslib_1.__assign(tslib_1.__assign({}, prevState.eventId), { status: types_1.EventIdStatus.NOT_FOUND }),
                        }); });
                        return [3 /*break*/, 4];
                    case 3:
                        _b = _c.sent();
                        this.setState(function (prevState) { return ({
                            eventId: tslib_1.__assign(tslib_1.__assign({}, prevState.eventId), { status: types_1.EventIdStatus.ERROR }),
                        }); });
                        return [3 /*break*/, 4];
                    case 4: return [2 /*return*/];
                }
            });
        });
    };
    ModalManager.prototype.convertRequestError = function (error) {
        switch (error.type) {
            case handleError_1.ErrorType.InvalidSelector:
                this.setState(function (prevState) { return ({
                    errors: tslib_1.__assign(tslib_1.__assign({}, prevState.errors), { source: error.message }),
                }); });
                break;
            case handleError_1.ErrorType.RegexParse:
                this.setState(function (prevState) { return ({
                    errors: tslib_1.__assign(tslib_1.__assign({}, prevState.errors), { pattern: error.message }),
                }); });
                break;
            default:
                indicator_1.addErrorMessage(error.message);
        }
    };
    ModalManager.prototype.handleValidateForm = function () {
        var _a = this.state, values = _a.values, requiredValues = _a.requiredValues;
        var isFormValid = requiredValues.every(function (requiredValue) { return !!values[requiredValue]; });
        this.setState({ isFormValid: isFormValid });
    };
    ModalManager.prototype.render = function () {
        var _a = this.state, values = _a.values, errors = _a.errors, isFormValid = _a.isFormValid, eventId = _a.eventId, sourceSuggestions = _a.sourceSuggestions;
        var title = this.props.title;
        return (<modal_1.default {...this.props} title={title} onSave={this.handleSave} disabled={!isFormValid} content={<form_1.default onChange={this.handleChange} onValidate={this.handleValidate} onUpdateEventId={this.handleUpdateEventId} eventId={eventId} errors={errors} values={values} sourceSuggestions={sourceSuggestions}/>}/>);
    };
    return ModalManager;
}(React.Component));
exports.default = ModalManager;
//# sourceMappingURL=modalManager.jsx.map
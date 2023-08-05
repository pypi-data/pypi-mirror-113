Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var omit_1 = tslib_1.__importDefault(require("lodash/omit"));
var indicator_1 = require("app/actionCreators/indicator");
var button_1 = tslib_1.__importDefault(require("app/components/button"));
var buttonBar_1 = tslib_1.__importDefault(require("app/components/buttonBar"));
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var dynamicSampling_1 = require("app/types/dynamicSampling");
var utils_1 = require("app/utils");
var numberField_1 = tslib_1.__importDefault(require("app/views/settings/components/forms/numberField"));
var radioField_1 = tslib_1.__importDefault(require("app/views/settings/components/forms/radioField"));
var conditionFields_1 = tslib_1.__importDefault(require("./conditionFields"));
var handleXhrErrorResponse_1 = tslib_1.__importDefault(require("./handleXhrErrorResponse"));
var utils_2 = require("./utils");
var transactionChoices = [
    [utils_2.Transaction.ALL, locale_1.t('Apply to all')],
    [utils_2.Transaction.MATCH_CONDITIONS, locale_1.t('Match custom conditions')],
];
var Form = /** @class */ (function (_super) {
    tslib_1.__extends(Form, _super);
    function Form() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = _this.getDefaultState();
        _this.handleChange = function (field, value) {
            _this.setState(function (prevState) {
                var _a;
                return (tslib_1.__assign(tslib_1.__assign({}, prevState), (_a = {}, _a[field] = value, _a)));
            });
        };
        _this.handleChangeTransaction = function (value) {
            _this.setState(function (prevState) { return ({
                transaction: value,
                conditions: value === utils_2.Transaction.ALL ? [] : prevState.conditions,
            }); });
        };
        _this.handleSubmit = function () {
            // Children have to implement this
            throw new Error('Not implemented');
        };
        _this.handleAddCondition = function () {
            var conditions = _this.state.conditions;
            var categoryOptions = _this.getCategoryOptions();
            if (!conditions.length) {
                _this.setState({
                    conditions: [
                        {
                            category: categoryOptions[0][0],
                            match: '',
                        },
                    ],
                });
                return;
            }
            var nextCategory = categoryOptions.find(function (categoryOption) {
                return !conditions.find(function (condition) { return condition.category === categoryOption[0]; });
            });
            if (!nextCategory) {
                return;
            }
            _this.setState({
                conditions: tslib_1.__spreadArray(tslib_1.__spreadArray([], tslib_1.__read(conditions)), [
                    {
                        category: nextCategory[0],
                        match: '',
                    },
                ]),
            });
        };
        _this.handleChangeCondition = function (index, field, value) {
            var newConditions = tslib_1.__spreadArray([], tslib_1.__read(_this.state.conditions));
            newConditions[index][field] = value;
            _this.setState({ conditions: newConditions });
        };
        _this.handleDeleteCondition = function (index) { return function () {
            var newConditions = tslib_1.__spreadArray([], tslib_1.__read(_this.state.conditions));
            newConditions.splice(index, 1);
            if (!newConditions.length) {
                _this.setState({
                    conditions: newConditions,
                    transaction: utils_2.Transaction.ALL,
                });
                return;
            }
            _this.setState({ conditions: newConditions });
        }; };
        return _this;
    }
    Form.prototype.componentDidUpdate = function (_prevProps, prevState) {
        if (prevState.transaction === utils_2.Transaction.ALL &&
            this.state.transaction !== utils_2.Transaction.ALL &&
            !this.state.conditions.length) {
            this.handleAddCondition();
        }
    };
    Form.prototype.getDefaultState = function () {
        var rule = this.props.rule;
        if (rule) {
            var _a = rule, conditions = _a.condition, sampleRate = _a.sampleRate;
            var inner = conditions.inner;
            return {
                transaction: !inner.length ? utils_2.Transaction.ALL : utils_2.Transaction.MATCH_CONDITIONS,
                conditions: inner.map(function (_a) {
                    var name = _a.name, value = _a.value;
                    if (Array.isArray(value)) {
                        if (utils_2.isLegacyBrowser(value)) {
                            return {
                                category: name,
                                legacyBrowsers: value,
                            };
                        }
                        return {
                            category: name,
                            match: value.join('\n'),
                        };
                    }
                    return { category: name };
                }),
                sampleRate: sampleRate * 100,
                errors: {},
            };
        }
        return {
            transaction: utils_2.Transaction.ALL,
            conditions: [],
            errors: {},
        };
    };
    Form.prototype.getNewCondition = function (condition) {
        var _a;
        // DynamicSamplingConditionLogicalInnerEqBoolean
        if (condition.category === dynamicSampling_1.DynamicSamplingInnerName.EVENT_BROWSER_EXTENSIONS ||
            condition.category === dynamicSampling_1.DynamicSamplingInnerName.EVENT_WEB_CRAWLERS ||
            condition.category === dynamicSampling_1.DynamicSamplingInnerName.EVENT_LOCALHOST) {
            return {
                op: dynamicSampling_1.DynamicSamplingInnerOperator.EQUAL,
                name: condition.category,
                value: true,
            };
        }
        // DynamicSamplingConditionLogicalInnerCustom
        if (condition.category === dynamicSampling_1.DynamicSamplingInnerName.EVENT_LEGACY_BROWSER) {
            return {
                op: dynamicSampling_1.DynamicSamplingInnerOperator.CUSTOM,
                name: condition.category,
                value: (_a = condition.legacyBrowsers) !== null && _a !== void 0 ? _a : [],
            };
        }
        var newValue = condition.match
            .split('\n')
            .filter(function (match) { return !!match.trim(); })
            .map(function (match) { return match.trim(); });
        if (condition.category === dynamicSampling_1.DynamicSamplingInnerName.EVENT_IP_ADDRESSES ||
            condition.category === dynamicSampling_1.DynamicSamplingInnerName.EVENT_ERROR_MESSAGES ||
            condition.category === dynamicSampling_1.DynamicSamplingInnerName.EVENT_CSP) {
            return {
                op: dynamicSampling_1.DynamicSamplingInnerOperator.CUSTOM,
                name: condition.category,
                value: newValue,
            };
        }
        // DynamicSamplingConditionLogicalInnerGlob
        if (condition.category === dynamicSampling_1.DynamicSamplingInnerName.EVENT_RELEASE ||
            condition.category === dynamicSampling_1.DynamicSamplingInnerName.TRACE_RELEASE) {
            return {
                op: dynamicSampling_1.DynamicSamplingInnerOperator.GLOB_MATCH,
                name: condition.category,
                value: newValue,
            };
        }
        // DynamicSamplingConditionLogicalInnerEq
        if (condition.category === dynamicSampling_1.DynamicSamplingInnerName.TRACE_USER_ID ||
            condition.category === dynamicSampling_1.DynamicSamplingInnerName.EVENT_USER_ID) {
            return {
                op: dynamicSampling_1.DynamicSamplingInnerOperator.EQUAL,
                name: condition.category,
                value: newValue,
                options: {
                    ignoreCase: false,
                },
            };
        }
        // DynamicSamplingConditionLogicalInnerEq
        return {
            op: dynamicSampling_1.DynamicSamplingInnerOperator.EQUAL,
            name: condition.category,
            value: newValue,
            options: {
                ignoreCase: true,
            },
        };
    };
    Form.prototype.getSuccessMessage = function () {
        var rule = this.props.rule;
        return rule
            ? locale_1.t('Successfully edited dynamic sampling rule')
            : locale_1.t('Successfully added dynamic sampling rule');
    };
    Form.prototype.clearError = function (field) {
        this.setState(function (state) { return ({
            errors: omit_1.default(state.errors, field),
        }); });
    };
    Form.prototype.convertErrorXhrResponse = function (error) {
        switch (error.type) {
            case 'sampleRate':
                this.setState(function (prevState) { return ({
                    errors: tslib_1.__assign(tslib_1.__assign({}, prevState.errors), { sampleRate: error.message }),
                }); });
                break;
            default:
                indicator_1.addErrorMessage(error.message);
        }
    };
    Form.prototype.submitRules = function (newRules, currentRuleIndex) {
        return tslib_1.__awaiter(this, void 0, void 0, function () {
            var _a, organization, project, api, onSubmitSuccess, closeModal, newProjectDetails, error_1;
            return tslib_1.__generator(this, function (_b) {
                switch (_b.label) {
                    case 0:
                        _a = this.props, organization = _a.organization, project = _a.project, api = _a.api, onSubmitSuccess = _a.onSubmitSuccess, closeModal = _a.closeModal;
                        _b.label = 1;
                    case 1:
                        _b.trys.push([1, 3, , 4]);
                        return [4 /*yield*/, api.requestPromise("/projects/" + organization.slug + "/" + project.slug + "/", { method: 'PUT', data: { dynamicSampling: { rules: newRules } } })];
                    case 2:
                        newProjectDetails = _b.sent();
                        onSubmitSuccess(newProjectDetails, this.getSuccessMessage());
                        closeModal();
                        return [3 /*break*/, 4];
                    case 3:
                        error_1 = _b.sent();
                        this.convertErrorXhrResponse(handleXhrErrorResponse_1.default(error_1, currentRuleIndex));
                        return [3 /*break*/, 4];
                    case 4: return [2 /*return*/];
                }
            });
        });
    };
    Form.prototype.getModalTitle = function () {
        return '';
    };
    Form.prototype.geTransactionFieldDescription = function () {
        return {
            label: '',
            // help: '', TODO(Priscila): Add correct descriptions
        };
    };
    Form.prototype.getExtraFields = function () {
        return null;
    };
    Form.prototype.getCategoryOptions = function () {
        // Children have to implement this
        throw new Error('Not implemented');
    };
    Form.prototype.render = function () {
        var _this = this;
        var _a = this.props, Header = _a.Header, Body = _a.Body, closeModal = _a.closeModal, Footer = _a.Footer;
        var _b = this.state, sampleRate = _b.sampleRate, conditions = _b.conditions, transaction = _b.transaction, errors = _b.errors;
        var transactionField = this.geTransactionFieldDescription();
        var categoryOptions = this.getCategoryOptions();
        var submitDisabled = !utils_1.defined(sampleRate) ||
            (!!conditions.length &&
                !!conditions.find(function (condition) {
                    var _a;
                    if (condition.category === dynamicSampling_1.DynamicSamplingInnerName.EVENT_LEGACY_BROWSER) {
                        return !((_a = condition.legacyBrowsers) !== null && _a !== void 0 ? _a : []).length;
                    }
                    if (condition.category === dynamicSampling_1.DynamicSamplingInnerName.EVENT_LOCALHOST ||
                        condition.category === dynamicSampling_1.DynamicSamplingInnerName.EVENT_BROWSER_EXTENSIONS ||
                        condition.category === dynamicSampling_1.DynamicSamplingInnerName.EVENT_WEB_CRAWLERS) {
                        return false;
                    }
                    return !condition.match;
                }));
        return (<React.Fragment>
        <Header closeButton>
          <h4>{this.getModalTitle()}</h4>
        </Header>
        <Body>
          <Fields>
            {this.getExtraFields()}
            <radioField_1.default {...transactionField} name="transaction" choices={transactionChoices} onChange={this.handleChangeTransaction} value={transaction} inline={false} hideControlState showHelpInTooltip stacked required/>
            {transaction !== utils_2.Transaction.ALL && (<conditionFields_1.default conditions={conditions} categoryOptions={categoryOptions} onAdd={this.handleAddCondition} onChange={this.handleChangeCondition} onDelete={this.handleDeleteCondition}/>)}
            <numberField_1.default label={locale_1.t('Sampling Rate')} 
        // help={t('this is a description')}  TODO(Priscila): Add correct descriptions
        name="sampleRate" onChange={function (value) {
                _this.handleChange('sampleRate', utils_1.defined(value) ? Number(value) : undefined);
                if (!!errors.sampleRate) {
                    _this.clearError('sampleRate');
                }
            }} placeholder={'\u0025'} value={!sampleRate ? undefined : sampleRate} inline={false} hideControlState={!errors.sampleRate} error={errors.sampleRate} showHelpInTooltip stacked required/>
          </Fields>
        </Body>
        <Footer>
          <buttonBar_1.default gap={1}>
            <button_1.default onClick={closeModal}>{locale_1.t('Cancel')}</button_1.default>
            <button_1.default priority="primary" onClick={this.handleSubmit} disabled={submitDisabled}>
              {locale_1.t('Save Rule')}
            </button_1.default>
          </buttonBar_1.default>
        </Footer>
      </React.Fragment>);
    };
    return Form;
}(React.Component));
exports.default = Form;
var Fields = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  display: grid;\n  grid-gap: ", ";\n"], ["\n  display: grid;\n  grid-gap: ", ";\n"])), space_1.default(1));
var templateObject_1;
//# sourceMappingURL=form.jsx.map
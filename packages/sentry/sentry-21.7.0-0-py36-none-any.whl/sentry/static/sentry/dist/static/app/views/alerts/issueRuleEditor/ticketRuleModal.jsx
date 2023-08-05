Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var indicator_1 = require("app/actionCreators/indicator");
var abstractExternalIssueForm_1 = tslib_1.__importDefault(require("app/components/externalIssues/abstractExternalIssueForm"));
var externalLink_1 = tslib_1.__importDefault(require("app/components/links/externalLink"));
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var TicketRuleModal = /** @class */ (function (_super) {
    tslib_1.__extends(TicketRuleModal, _super);
    function TicketRuleModal() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.handleReceiveIntegrationDetails = function (integrationDetails) {
            _this.setState({
                issueConfigFieldsCache: integrationDetails[_this.getConfigName()],
            });
        };
        /**
         * Get a list of formFields names with valid config data.
         */
        _this.getValidAndSavableFieldNames = function () {
            var issueConfigFieldsCache = _this.state.issueConfigFieldsCache;
            return (issueConfigFieldsCache || [])
                .filter(function (field) { return field.hasOwnProperty('name'); })
                .map(function (field) { return field.name; });
        };
        /**
         * Clean up the form data before saving it to state.
         */
        _this.cleanData = function (data) {
            var e_1, _a;
            var instance = _this.props.instance;
            var issueConfigFieldsCache = _this.state.issueConfigFieldsCache;
            var names = _this.getValidAndSavableFieldNames();
            var formData = {};
            if (instance === null || instance === void 0 ? void 0 : instance.hasOwnProperty('integration')) {
                formData.integration = instance.integration;
            }
            formData.dynamic_form_fields = issueConfigFieldsCache;
            try {
                for (var _b = tslib_1.__values(Object.entries(data)), _c = _b.next(); !_c.done; _c = _b.next()) {
                    var _d = tslib_1.__read(_c.value, 2), key = _d[0], value = _d[1];
                    if (names.includes(key)) {
                        formData[key] = value;
                    }
                }
            }
            catch (e_1_1) { e_1 = { error: e_1_1 }; }
            finally {
                try {
                    if (_c && !_c.done && (_a = _b.return)) _a.call(_b);
                }
                finally { if (e_1) throw e_1.error; }
            }
            return formData;
        };
        _this.onFormSubmit = function (data, _success, _error, e, model) {
            var _a = _this.props, onSubmitAction = _a.onSubmitAction, closeModal = _a.closeModal;
            var fetchedFieldOptionsCache = _this.state.fetchedFieldOptionsCache;
            // This is a "fake form", so don't actually POST to an endpoint.
            e.preventDefault();
            e.stopPropagation();
            if (model.validateForm()) {
                onSubmitAction(_this.cleanData(data), fetchedFieldOptionsCache);
                indicator_1.addSuccessMessage(locale_1.t('Changes applied.'));
                closeModal();
            }
        };
        _this.getFormProps = function () {
            var closeModal = _this.props.closeModal;
            return tslib_1.__assign(tslib_1.__assign({}, _this.getDefaultFormProps()), { cancelLabel: locale_1.t('Close'), onCancel: closeModal, onSubmit: _this.onFormSubmit, submitLabel: locale_1.t('Apply Changes') });
        };
        /**
         * Set the initial data from the Rule, replace `title` and `description` with
         * disabled inputs, and use the cached dynamic choices.
         */
        _this.cleanFields = function () {
            var instance = _this.props.instance;
            var fields = [
                {
                    name: 'title',
                    label: 'Title',
                    type: 'string',
                    default: 'This will be the same as the Sentry Issue.',
                    disabled: true,
                },
                {
                    name: 'description',
                    label: 'Description',
                    type: 'string',
                    default: 'This will be generated from the Sentry Issue details.',
                    disabled: true,
                },
            ];
            return fields.concat(_this.getCleanedFields()
                // Skip fields if they already exist.
                .filter(function (field) { return !fields.map(function (f) { return f.name; }).includes(field.name); })
                .map(function (field) {
                // Overwrite defaults from cache.
                if (instance.hasOwnProperty(field.name)) {
                    field.default = instance[field.name] || field.default;
                }
                return field;
            }));
        };
        _this.renderBodyText = function () {
            // `ticketType` already includes indefinite article.
            var _a = _this.props, ticketType = _a.ticketType, link = _a.link;
            return (<BodyText>
        {locale_1.tct('When this alert is triggered [ticketType] will be ' +
                    'created with the following fields. It will also [linkToDocs] ' +
                    'with the new Sentry Issue.', {
                    linkToDocs: <externalLink_1.default href={link}>{locale_1.t('stay in sync')}</externalLink_1.default>,
                    ticketType: ticketType,
                })}
      </BodyText>);
        };
        return _this;
    }
    TicketRuleModal.prototype.getDefaultState = function () {
        var instance = this.props.instance;
        var issueConfigFieldsCache = Object.values((instance === null || instance === void 0 ? void 0 : instance.dynamic_form_fields) || {});
        return tslib_1.__assign(tslib_1.__assign({}, _super.prototype.getDefaultState.call(this)), { fetchedFieldOptionsCache: Object.fromEntries(issueConfigFieldsCache.map(function (field) { return [field.name, field.choices]; })), issueConfigFieldsCache: issueConfigFieldsCache });
    };
    TicketRuleModal.prototype.getEndpoints = function () {
        var instance = this.props.instance;
        var query = (instance.dynamic_form_fields || [])
            .filter(function (field) { return field.updatesForm; })
            .filter(function (field) { return instance.hasOwnProperty(field.name); })
            .reduce(function (accumulator, _a) {
            var name = _a.name;
            accumulator[name] = instance[name];
            return accumulator;
        }, { action: 'create' });
        return [['integrationDetails', this.getEndPointString(), { query: query }]];
    };
    TicketRuleModal.prototype.getEndPointString = function () {
        var _a = this.props, instance = _a.instance, organization = _a.organization;
        return "/organizations/" + organization.slug + "/integrations/" + instance.integration + "/";
    };
    TicketRuleModal.prototype.render = function () {
        return this.renderForm(this.cleanFields());
    };
    return TicketRuleModal;
}(abstractExternalIssueForm_1.default));
var BodyText = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  margin-bottom: ", ";\n"], ["\n  margin-bottom: ", ";\n"])), space_1.default(3));
exports.default = TicketRuleModal;
var templateObject_1;
//# sourceMappingURL=ticketRuleModal.jsx.map
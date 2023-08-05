Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var Sentry = tslib_1.__importStar(require("@sentry/react"));
var indicator_1 = require("app/actionCreators/indicator");
var abstractExternalIssueForm_1 = tslib_1.__importDefault(require("app/components/externalIssues/abstractExternalIssueForm"));
var navTabs_1 = tslib_1.__importDefault(require("app/components/navTabs"));
var locale_1 = require("app/locale");
var MESSAGES_BY_ACTION = {
    link: locale_1.t('Successfully linked issue.'),
    create: locale_1.t('Successfully created issue.'),
};
var SUBMIT_LABEL_BY_ACTION = {
    link: locale_1.t('Link Issue'),
    create: locale_1.t('Create Issue'),
};
var ExternalIssueForm = /** @class */ (function (_super) {
    tslib_1.__extends(ExternalIssueForm, _super);
    function ExternalIssueForm(props) {
        var _this = _super.call(this, props, {}) || this;
        _this.handleClick = function (action) {
            _this.setState({ action: action }, function () { return _this.reloadData(); });
        };
        _this.startTransaction = function (type) {
            var _a = _this.props, group = _a.group, integration = _a.integration;
            var action = _this.state.action;
            var transaction = Sentry.startTransaction({ name: "externalIssueForm." + type });
            Sentry.getCurrentHub().configureScope(function (scope) { return scope.setSpan(transaction); });
            transaction.setTag('issueAction', action);
            transaction.setTag('groupID', group.id);
            transaction.setTag('projectID', group.project.id);
            transaction.setTag('integrationSlug', integration.provider.slug);
            transaction.setTag('integrationType', 'firstParty');
            return transaction;
        };
        _this.handlePreSubmit = function () {
            _this.submitTransaction = _this.startTransaction('submit');
        };
        _this.onSubmitSuccess = function (_data) {
            var _a;
            var _b = _this.props, onChange = _b.onChange, closeModal = _b.closeModal;
            var action = _this.state.action;
            onChange(function () { return indicator_1.addSuccessMessage(MESSAGES_BY_ACTION[action]); });
            closeModal();
            (_a = _this.submitTransaction) === null || _a === void 0 ? void 0 : _a.finish();
        };
        _this.handleSubmitError = function () {
            var _a;
            (_a = _this.submitTransaction) === null || _a === void 0 ? void 0 : _a.finish();
        };
        _this.onLoadAllEndpointsSuccess = function () {
            var _a;
            (_a = _this.loadTransaction) === null || _a === void 0 ? void 0 : _a.finish();
        };
        _this.onRequestError = function () {
            var _a;
            (_a = _this.loadTransaction) === null || _a === void 0 ? void 0 : _a.finish();
        };
        _this.getTitle = function () {
            var integration = _this.props.integration;
            return locale_1.tct('[integration] Issue', { integration: integration.provider.name });
        };
        _this.getFormProps = function () {
            var action = _this.state.action;
            return tslib_1.__assign(tslib_1.__assign({}, _this.getDefaultFormProps()), { submitLabel: SUBMIT_LABEL_BY_ACTION[action], apiEndpoint: _this.getEndPointString(), apiMethod: action === 'create' ? 'POST' : 'PUT', onPreSubmit: _this.handlePreSubmit, onSubmitError: _this.handleSubmitError, onSubmitSuccess: _this.onSubmitSuccess });
        };
        _this.renderNavTabs = function () {
            var action = _this.state.action;
            return (<navTabs_1.default underlined>
        <li className={action === 'create' ? 'active' : ''}>
          <a onClick={function () { return _this.handleClick('create'); }}>{locale_1.t('Create')}</a>
        </li>
        <li className={action === 'link' ? 'active' : ''}>
          <a onClick={function () { return _this.handleClick('link'); }}>{locale_1.t('Link')}</a>
        </li>
      </navTabs_1.default>);
        };
        _this.loadTransaction = _this.startTransaction('load');
        return _this;
    }
    ExternalIssueForm.prototype.getEndpoints = function () {
        var _a;
        var query = {};
        if ((_a = this.state) === null || _a === void 0 ? void 0 : _a.hasOwnProperty('action')) {
            query.action = this.state.action;
        }
        return [['integrationDetails', this.getEndPointString(), { query: query }]];
    };
    ExternalIssueForm.prototype.getEndPointString = function () {
        var _a = this.props, group = _a.group, integration = _a.integration;
        return "/groups/" + group.id + "/integrations/" + integration.id + "/";
    };
    ExternalIssueForm.prototype.renderBody = function () {
        return this.renderForm(this.getCleanedFields());
    };
    return ExternalIssueForm;
}(abstractExternalIssueForm_1.default));
exports.default = ExternalIssueForm;
//# sourceMappingURL=externalIssueForm.jsx.map
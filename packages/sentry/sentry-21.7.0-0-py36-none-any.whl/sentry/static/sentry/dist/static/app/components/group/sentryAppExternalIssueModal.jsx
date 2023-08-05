Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var sentryAppExternalIssueForm_1 = tslib_1.__importDefault(require("app/components/group/sentryAppExternalIssueForm"));
var navTabs_1 = tslib_1.__importDefault(require("app/components/navTabs"));
var locale_1 = require("app/locale");
var withApi_1 = tslib_1.__importDefault(require("app/utils/withApi"));
var SentryAppExternalIssueModal = /** @class */ (function (_super) {
    tslib_1.__extends(SentryAppExternalIssueModal, _super);
    function SentryAppExternalIssueModal() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            action: 'create',
        };
        _this.showLink = function () {
            _this.setState({ action: 'link' });
        };
        _this.showCreate = function () {
            _this.setState({ action: 'create' });
        };
        _this.onSubmitSuccess = function (externalIssue) {
            _this.props.onSubmitSuccess(externalIssue);
            _this.props.closeModal();
        };
        return _this;
    }
    SentryAppExternalIssueModal.prototype.render = function () {
        var _a = this.props, Header = _a.Header, Body = _a.Body, sentryAppComponent = _a.sentryAppComponent, sentryAppInstallation = _a.sentryAppInstallation, group = _a.group;
        var action = this.state.action;
        var name = sentryAppComponent.sentryApp.name;
        var config = sentryAppComponent.schema[action];
        return (<react_1.Fragment>
        <Header closeButton>{locale_1.tct('[name] Issue', { name: name })}</Header>
        <navTabs_1.default underlined>
          <li className={action === 'create' ? 'active create' : 'create'}>
            <a onClick={this.showCreate}>{locale_1.t('Create')}</a>
          </li>
          <li className={action === 'link' ? 'active link' : 'link'}>
            <a onClick={this.showLink}>{locale_1.t('Link')}</a>
          </li>
        </navTabs_1.default>
        <Body>
          <sentryAppExternalIssueForm_1.default group={group} sentryAppInstallation={sentryAppInstallation} appName={name} config={config} action={action} onSubmitSuccess={this.onSubmitSuccess} event={this.props.event}/>
        </Body>
      </react_1.Fragment>);
    };
    return SentryAppExternalIssueModal;
}(react_1.Component));
exports.default = withApi_1.default(SentryAppExternalIssueModal);
//# sourceMappingURL=sentryAppExternalIssueModal.jsx.map
Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var performance_1 = require("app/actionCreators/performance");
var button_1 = tslib_1.__importDefault(require("app/components/button"));
var icons_1 = require("app/icons");
var locale_1 = require("app/locale");
var analytics_1 = require("app/utils/analytics");
var withApi_1 = tslib_1.__importDefault(require("app/utils/withApi"));
var KeyTransactionButton = /** @class */ (function (_super) {
    tslib_1.__extends(KeyTransactionButton, _super);
    function KeyTransactionButton() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            isLoading: true,
            keyFetchID: undefined,
            error: null,
            isKeyTransaction: false,
        };
        _this.fetchData = function () {
            var _a = _this.props, organization = _a.organization, eventView = _a.eventView, transactionName = _a.transactionName;
            var projects = eventView.project;
            if (projects.length !== 1) {
                return;
            }
            var url = "/organizations/" + organization.slug + "/is-key-transactions/";
            var keyFetchID = Symbol('keyFetchID');
            _this.setState({ isLoading: true, keyFetchID: keyFetchID });
            _this.props.api
                .requestPromise(url, {
                method: 'GET',
                includeAllArgs: true,
                query: {
                    project: projects.map(function (id) { return String(id); }),
                    transaction: transactionName,
                },
            })
                .then(function (_a) {
                var _b = tslib_1.__read(_a, 3), data = _b[0], _ = _b[1], _jqXHR = _b[2];
                if (_this.state.keyFetchID !== keyFetchID) {
                    // invariant: a different request was initiated after this request
                    return;
                }
                _this.setState({
                    isLoading: false,
                    keyFetchID: undefined,
                    error: null,
                    isKeyTransaction: !!(data === null || data === void 0 ? void 0 : data.isKey),
                });
            })
                .catch(function (err) {
                var _a, _b;
                _this.setState({
                    isLoading: false,
                    keyFetchID: undefined,
                    error: (_b = (_a = err.responseJSON) === null || _a === void 0 ? void 0 : _a.detail) !== null && _b !== void 0 ? _b : null,
                    isKeyTransaction: false,
                });
            });
        };
        _this.toggleKeyTransactionHandler = function () {
            var _a = _this.props, eventView = _a.eventView, api = _a.api, organization = _a.organization, transactionName = _a.transactionName;
            var isKeyTransaction = _this.state.isKeyTransaction;
            var projects = eventView.project.map(String);
            analytics_1.trackAnalyticsEvent({
                eventName: 'Performance Views: Key Transaction toggle',
                eventKey: 'performance_views.key_transaction.toggle',
                organization_id: organization.id,
                action: isKeyTransaction ? 'remove' : 'add',
            });
            performance_1.toggleKeyTransaction(api, isKeyTransaction, organization.slug, projects, transactionName).then(function () {
                _this.setState({ isKeyTransaction: !isKeyTransaction });
            });
        };
        return _this;
    }
    KeyTransactionButton.prototype.componentDidMount = function () {
        this.fetchData();
    };
    KeyTransactionButton.prototype.componentDidUpdate = function (prevProps) {
        var orgSlugChanged = prevProps.organization.slug !== this.props.organization.slug;
        var projectsChanged = prevProps.eventView.project.length === 1 &&
            this.props.eventView.project.length === 1 &&
            prevProps.eventView.project[0] !== this.props.eventView.project[0];
        if (orgSlugChanged || projectsChanged) {
            this.fetchData();
        }
    };
    KeyTransactionButton.prototype.render = function () {
        var _a = this.state, isKeyTransaction = _a.isKeyTransaction, isLoading = _a.isLoading;
        if (this.props.eventView.project.length !== 1 || isLoading) {
            return null;
        }
        return (<button_1.default icon={isKeyTransaction ? <icons_1.IconStar color="yellow300" isSolid/> : <icons_1.IconStar />} onClick={this.toggleKeyTransactionHandler}>
        {locale_1.t('Key Transaction')}
      </button_1.default>);
    };
    return KeyTransactionButton;
}(react_1.Component));
exports.default = withApi_1.default(KeyTransactionButton);
//# sourceMappingURL=keyTransactionButton.jsx.map
Object.defineProperty(exports, "__esModule", { value: true });
exports.DataExport = exports.ExportQueryType = void 0;
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var debounce_1 = tslib_1.__importDefault(require("lodash/debounce"));
var isEqual_1 = tslib_1.__importDefault(require("lodash/isEqual"));
var indicator_1 = require("app/actionCreators/indicator");
var feature_1 = tslib_1.__importDefault(require("app/components/acl/feature"));
var button_1 = tslib_1.__importDefault(require("app/components/button"));
var locale_1 = require("app/locale");
var withApi_1 = tslib_1.__importDefault(require("app/utils/withApi"));
var withOrganization_1 = tslib_1.__importDefault(require("app/utils/withOrganization"));
// NOTE: Coordinate with other ExportQueryType (src/sentry/data_export/base.py)
var ExportQueryType;
(function (ExportQueryType) {
    ExportQueryType["IssuesByTag"] = "Issues-by-Tag";
    ExportQueryType["Discover"] = "Discover";
})(ExportQueryType = exports.ExportQueryType || (exports.ExportQueryType = {}));
var DataExport = /** @class */ (function (_super) {
    tslib_1.__extends(DataExport, _super);
    function DataExport() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = _this.initialState;
        _this.resetState = function () {
            _this.setState(_this.initialState);
        };
        _this.startDataExport = function () {
            var _a = _this.props, api = _a.api, slug = _a.organization.slug, _b = _a.payload, queryType = _b.queryType, queryInfo = _b.queryInfo;
            _this.setState({ inProgress: true });
            api
                .requestPromise("/organizations/" + slug + "/data-export/", {
                includeAllArgs: true,
                method: 'POST',
                data: {
                    query_type: queryType,
                    query_info: queryInfo,
                },
            })
                .then(function (_a) {
                var _b = tslib_1.__read(_a, 3), _data = _b[0], _ = _b[1], response = _b[2];
                indicator_1.addSuccessMessage((response === null || response === void 0 ? void 0 : response.status) === 201
                    ? locale_1.t("Sit tight. We'll shoot you an email when your data is ready for download.")
                    : locale_1.t("It looks like we're already working on it. Sit tight, we'll email you."));
            })
                .catch(function (err) {
                var _a, _b;
                var message = (_b = (_a = err === null || err === void 0 ? void 0 : err.responseJSON) === null || _a === void 0 ? void 0 : _a.detail) !== null && _b !== void 0 ? _b : "We tried our hardest, but we couldn't export your data. Give it another go.";
                indicator_1.addErrorMessage(locale_1.t(message));
                _this.setState({ inProgress: false });
            });
        };
        return _this;
    }
    DataExport.prototype.componentDidUpdate = function (_a) {
        var prevPayload = _a.payload;
        var payload = this.props.payload;
        if (!isEqual_1.default(prevPayload, payload))
            this.resetState();
    };
    Object.defineProperty(DataExport.prototype, "initialState", {
        get: function () {
            return {
                inProgress: false,
            };
        },
        enumerable: false,
        configurable: true
    });
    DataExport.prototype.render = function () {
        var inProgress = this.state.inProgress;
        var _a = this.props, children = _a.children, disabled = _a.disabled, icon = _a.icon;
        return (<feature_1.default features={['organizations:discover-query']}>
        {inProgress ? (<button_1.default size="small" priority="default" title="You can get on with your life. We'll email you when your data's ready." {...this.props} disabled icon={icon}>
            {locale_1.t("We're working on it...")}
          </button_1.default>) : (<button_1.default onClick={debounce_1.default(this.startDataExport, 500)} disabled={disabled || false} size="small" priority="default" title="Put your data to work. Start your export and we'll email you when it's finished." icon={icon} {...this.props}>
            {children ? children : locale_1.t('Export All to CSV')}
          </button_1.default>)}
      </feature_1.default>);
    };
    return DataExport;
}(React.Component));
exports.DataExport = DataExport;
exports.default = withApi_1.default(withOrganization_1.default(DataExport));
//# sourceMappingURL=dataExport.jsx.map
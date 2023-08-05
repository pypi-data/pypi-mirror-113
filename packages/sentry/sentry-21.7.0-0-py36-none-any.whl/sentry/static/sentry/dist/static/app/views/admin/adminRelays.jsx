Object.defineProperty(exports, "__esModule", { value: true });
exports.AdminRelays = void 0;
var tslib_1 = require("tslib");
var react_1 = require("react");
var moment_1 = tslib_1.__importDefault(require("moment"));
var linkWithConfirmation_1 = tslib_1.__importDefault(require("app/components/links/linkWithConfirmation"));
var resultGrid_1 = tslib_1.__importDefault(require("app/components/resultGrid"));
var locale_1 = require("app/locale");
var withApi_1 = tslib_1.__importDefault(require("app/utils/withApi"));
var prettyDate = function (x) { return moment_1.default(x).format('ll LTS'); };
var AdminRelays = /** @class */ (function (_super) {
    tslib_1.__extends(AdminRelays, _super);
    function AdminRelays() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            loading: false,
        };
        return _this;
    }
    AdminRelays.prototype.onDelete = function (key) {
        var _this = this;
        this.setState({ loading: true });
        this.props.api.request("/relays/" + key + "/", {
            method: 'DELETE',
            success: function () { return _this.setState({ loading: false }); },
            error: function () { return _this.setState({ loading: false }); },
        });
    };
    AdminRelays.prototype.getRow = function (row) {
        var _this = this;
        return [
            <td key="id">
        <strong>{row.relayId}</strong>
      </td>,
            <td key="key">{row.publicKey}</td>,
            <td key="firstSeen" style={{ textAlign: 'right' }}>
        {prettyDate(row.firstSeen)}
      </td>,
            <td key="lastSeen" style={{ textAlign: 'right' }}>
        {prettyDate(row.lastSeen)}
      </td>,
            <td key="tools" style={{ textAlign: 'right' }}>
        <span className="editor-tools">
          <linkWithConfirmation_1.default className="danger" title="Remove" message={locale_1.t('Are you sure you wish to delete this relay?')} onConfirm={function () { return _this.onDelete(row.id); }}>
            {locale_1.t('Remove')}
          </linkWithConfirmation_1.default>
        </span>
      </td>,
        ];
    };
    AdminRelays.prototype.render = function () {
        var columns = [
            <th key="id" style={{ width: 350, textAlign: 'left' }}>
        Relay
      </th>,
            <th key="key">Public Key</th>,
            <th key="firstSeen" style={{ width: 150, textAlign: 'right' }}>
        First seen
      </th>,
            <th key="lastSeen" style={{ width: 150, textAlign: 'right' }}>
        Last seen
      </th>,
            <th key="tools"/>,
        ];
        return (<div>
        <h3>{locale_1.t('Relays')}</h3>
        <resultGrid_1.default path="/manage/relays/" endpoint="/relays/" method="GET" columns={columns} columnsForRow={this.getRow} hasSearch={false} sortOptions={[
                ['firstSeen', 'First seen'],
                ['lastSeen', 'Last seen'],
                ['relayId', 'Relay ID'],
            ]} defaultSort="firstSeen" {...this.props}/>
      </div>);
    };
    return AdminRelays;
}(react_1.Component));
exports.AdminRelays = AdminRelays;
exports.default = withApi_1.default(AdminRelays);
//# sourceMappingURL=adminRelays.jsx.map
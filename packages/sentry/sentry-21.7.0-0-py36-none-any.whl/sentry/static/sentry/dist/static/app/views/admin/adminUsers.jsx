Object.defineProperty(exports, "__esModule", { value: true });
exports.prettyDate = void 0;
var tslib_1 = require("tslib");
var moment_1 = tslib_1.__importDefault(require("moment"));
var link_1 = tslib_1.__importDefault(require("app/components/links/link"));
var resultGrid_1 = tslib_1.__importDefault(require("app/components/resultGrid"));
var locale_1 = require("app/locale");
var asyncView_1 = tslib_1.__importDefault(require("app/views/asyncView"));
var prettyDate = function (x) {
    return moment_1.default(x).format('ll');
};
exports.prettyDate = prettyDate;
var AdminUsers = /** @class */ (function (_super) {
    tslib_1.__extends(AdminUsers, _super);
    function AdminUsers() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.getRow = function (row) { return [
            <td key="username">
      <strong>
        <link_1.default to={"/manage/users/" + row.id + "/"}>{row.username}</link_1.default>
      </strong>
      <br />
      {row.email !== row.username && <small>{row.email}</small>}
    </td>,
            <td key="dateJoined" style={{ textAlign: 'center' }}>
      {exports.prettyDate(row.dateJoined)}
    </td>,
            <td key="lastLogin" style={{ textAlign: 'center' }}>
      {exports.prettyDate(row.lastLogin)}
    </td>,
        ]; };
        return _this;
    }
    AdminUsers.prototype.render = function () {
        var columns = [
            <th key="username">User</th>,
            <th key="dateJoined" style={{ textAlign: 'center', width: 150 }}>
        Joined
      </th>,
            <th key="lastLogin" style={{ textAlign: 'center', width: 150 }}>
        Last Login
      </th>,
        ];
        return (<div>
        <h3>{locale_1.t('Users')}</h3>
        <resultGrid_1.default path="/manage/users/" endpoint="/users/" method="GET" columns={columns} columnsForRow={this.getRow} hasSearch filters={{
                status: {
                    name: 'Status',
                    options: [
                        ['active', 'Active'],
                        ['disabled', 'Disabled'],
                    ],
                },
            }} sortOptions={[['date', 'Date Joined']]} defaultSort="date" {...this.props}/>
      </div>);
    };
    return AdminUsers;
}(asyncView_1.default));
exports.default = AdminUsers;
//# sourceMappingURL=adminUsers.jsx.map
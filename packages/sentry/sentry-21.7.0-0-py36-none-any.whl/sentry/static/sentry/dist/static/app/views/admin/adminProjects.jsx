Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var moment_1 = tslib_1.__importDefault(require("moment"));
var resultGrid_1 = tslib_1.__importDefault(require("app/components/resultGrid"));
var locale_1 = require("app/locale");
var asyncView_1 = tslib_1.__importDefault(require("app/views/asyncView"));
var AdminProjects = /** @class */ (function (_super) {
    tslib_1.__extends(AdminProjects, _super);
    function AdminProjects() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.getRow = function (row) { return [
            <td key="name">
      <strong>
        <a href={"/" + row.organization.slug + "/" + row.slug + "/"}>{row.name}</a>
      </strong>
      <br />
      <small>{row.organization.name}</small>
    </td>,
            <td key="status" style={{ textAlign: 'center' }}>
      {row.status}
    </td>,
            <td key="dateCreated" style={{ textAlign: 'right' }}>
      {moment_1.default(row.dateCreated).format('ll')}
    </td>,
        ]; };
        return _this;
    }
    AdminProjects.prototype.render = function () {
        var columns = [
            <th key="name">Project</th>,
            <th key="status" style={{ width: 150, textAlign: 'center' }}>
        Status
      </th>,
            <th key="dateCreated" style={{ width: 200, textAlign: 'right' }}>
        Created
      </th>,
        ];
        return (<div>
        <h3>{locale_1.t('Projects')}</h3>
        <resultGrid_1.default path="/manage/projects/" endpoint="/projects/?show=all" method="GET" columns={columns} columnsForRow={this.getRow} hasSearch filters={{
                status: {
                    name: 'Status',
                    options: [
                        ['active', 'Active'],
                        ['deleted', 'Deleted'],
                    ],
                },
            }} sortOptions={[['date', 'Date Created']]} defaultSort="date" {...this.props}/>
      </div>);
    };
    return AdminProjects;
}(asyncView_1.default));
exports.default = AdminProjects;
//# sourceMappingURL=adminProjects.jsx.map
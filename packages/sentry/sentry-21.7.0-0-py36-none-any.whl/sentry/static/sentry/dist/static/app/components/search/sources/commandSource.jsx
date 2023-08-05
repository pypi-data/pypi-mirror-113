Object.defineProperty(exports, "__esModule", { value: true });
exports.CommandSource = void 0;
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var modal_1 = require("app/actionCreators/modal");
var access_1 = tslib_1.__importDefault(require("app/components/acl/access"));
var locale_1 = require("app/locale");
var configStore_1 = tslib_1.__importDefault(require("app/stores/configStore"));
var createFuzzySearch_1 = require("app/utils/createFuzzySearch");
var ACTIONS = [
    {
        title: 'Open Sudo Modal',
        description: 'Open Sudo Modal to re-identify yourself.',
        requiresSuperuser: false,
        action: function () {
            return modal_1.openSudo({
                sudo: true,
            });
        },
    },
    {
        title: 'Open Superuser Modal',
        description: 'Open Superuser Modal to re-identify yourself.',
        requiresSuperuser: true,
        action: function () {
            return modal_1.openSudo({
                superuser: true,
            });
        },
    },
    {
        title: 'Toggle dark mode',
        description: 'Toggle dark mode (superuser only atm)',
        requiresSuperuser: true,
        action: function () {
            return configStore_1.default.set('theme', configStore_1.default.get('theme') === 'dark' ? 'light' : 'dark');
        },
    },
    {
        title: 'Toggle Translation Markers',
        description: 'Toggles translation markers on or off in the application',
        requiresSuperuser: true,
        action: function () {
            locale_1.toggleLocaleDebug();
            window.location.reload();
        },
    },
    {
        title: 'Search Documentation and FAQ',
        description: 'Open the Documentation and FAQ search modal.',
        requiresSuperuser: false,
        action: function () {
            modal_1.openHelpSearchModal();
        },
    },
];
/**
 * This source is a hardcoded list of action creators and/or routes maybe
 */
var CommandSource = /** @class */ (function (_super) {
    tslib_1.__extends(CommandSource, _super);
    function CommandSource() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            fuzzy: null,
        };
        return _this;
    }
    CommandSource.prototype.componentDidMount = function () {
        this.createSearch(ACTIONS);
    };
    CommandSource.prototype.createSearch = function (searchMap) {
        return tslib_1.__awaiter(this, void 0, void 0, function () {
            var options, _a;
            var _b;
            return tslib_1.__generator(this, function (_c) {
                switch (_c.label) {
                    case 0:
                        options = tslib_1.__assign(tslib_1.__assign({}, this.props.searchOptions), { keys: ['title', 'description'] });
                        _a = this.setState;
                        _b = {};
                        return [4 /*yield*/, createFuzzySearch_1.createFuzzySearch(searchMap || [], options)];
                    case 1:
                        _a.apply(this, [(_b.fuzzy = _c.sent(),
                                _b)]);
                        return [2 /*return*/];
                }
            });
        });
    };
    CommandSource.prototype.render = function () {
        var _a = this.props, searchMap = _a.searchMap, query = _a.query, isSuperuser = _a.isSuperuser, children = _a.children;
        var results = [];
        if (this.state.fuzzy) {
            var rawResults = this.state.fuzzy.search(query);
            results = rawResults
                .filter(function (_a) {
                var item = _a.item;
                return !item.requiresSuperuser || isSuperuser;
            })
                .map(function (value) {
                var item = value.item, rest = tslib_1.__rest(value, ["item"]);
                return tslib_1.__assign({ item: tslib_1.__assign(tslib_1.__assign({}, item), { sourceType: 'command', resultType: 'command' }) }, rest);
            });
        }
        return children({
            isLoading: searchMap === null,
            results: results,
        });
    };
    CommandSource.defaultProps = {
        searchMap: [],
        searchOptions: {},
    };
    return CommandSource;
}(React.Component));
exports.CommandSource = CommandSource;
var CommandSourceWithFeature = function (props) { return (<access_1.default isSuperuser>
    {function (_a) {
    var hasSuperuser = _a.hasSuperuser;
    return <CommandSource {...props} isSuperuser={hasSuperuser}/>;
}}
  </access_1.default>); };
exports.default = CommandSourceWithFeature;
//# sourceMappingURL=commandSource.jsx.map
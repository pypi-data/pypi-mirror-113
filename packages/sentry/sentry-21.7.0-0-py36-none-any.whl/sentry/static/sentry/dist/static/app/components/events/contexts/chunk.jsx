Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var eventDataSection_1 = tslib_1.__importDefault(require("app/components/events/eventDataSection"));
var locale_1 = require("app/locale");
var plugins_1 = tslib_1.__importDefault(require("app/plugins"));
var utils_1 = require("app/utils");
var utils_2 = require("./utils");
var Chunk = /** @class */ (function (_super) {
    tslib_1.__extends(Chunk, _super);
    function Chunk() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            isLoading: false,
        };
        return _this;
    }
    Chunk.prototype.UNSAFE_componentWillMount = function () {
        this.syncPlugin();
    };
    Chunk.prototype.componentDidUpdate = function (prevProps) {
        var _a, _b;
        if (prevProps.type !== this.props.type ||
            ((_a = prevProps.group) === null || _a === void 0 ? void 0 : _a.id) !== ((_b = this.props.group) === null || _b === void 0 ? void 0 : _b.id)) {
            this.syncPlugin();
        }
    };
    Chunk.prototype.syncPlugin = function () {
        var _this = this;
        var _a = this.props, group = _a.group, type = _a.type, alias = _a.alias;
        // If we don't have a grouped event we can't sync with plugins.
        if (!group) {
            return;
        }
        // Search using `alias` first because old plugins rely on it and type is set to "default"
        // e.g. sessionstack
        var sourcePlugin = type === 'default'
            ? utils_2.getSourcePlugin(group.pluginContexts, alias) ||
                utils_2.getSourcePlugin(group.pluginContexts, type)
            : utils_2.getSourcePlugin(group.pluginContexts, type);
        if (!sourcePlugin) {
            this.setState({ pluginLoading: false });
            return;
        }
        this.setState({
            pluginLoading: true,
        }, function () {
            plugins_1.default.load(sourcePlugin, function () {
                _this.setState({ pluginLoading: false });
            });
        });
    };
    Chunk.prototype.getTitle = function () {
        var _a = this.props, _b = _a.value, value = _b === void 0 ? {} : _b, alias = _a.alias, type = _a.type;
        if (utils_1.defined(value.title) && typeof value.title !== 'object') {
            return value.title;
        }
        if (!utils_1.defined(type)) {
            return utils_1.toTitleCase(alias);
        }
        switch (type) {
            case 'app':
                return locale_1.t('App');
            case 'device':
                return locale_1.t('Device');
            case 'os':
                return locale_1.t('Operating System');
            case 'user':
                return locale_1.t('User');
            case 'gpu':
                return locale_1.t('Graphics Processing Unit');
            case 'runtime':
                return locale_1.t('Runtime');
            case 'trace':
                return locale_1.t('Trace Details');
            case 'default':
                if (alias === 'state')
                    return locale_1.t('Application State');
                return utils_1.toTitleCase(alias);
            default:
                return utils_1.toTitleCase(type);
        }
    };
    Chunk.prototype.render = function () {
        var pluginLoading = this.state.pluginLoading;
        // if we are currently loading the plugin, just render nothing for now.
        if (pluginLoading) {
            return null;
        }
        var _a = this.props, type = _a.type, alias = _a.alias, _b = _a.value, value = _b === void 0 ? {} : _b, event = _a.event;
        // we intentionally hide reprocessing context to not imply it was sent by the SDK.
        if (alias === 'reprocessing') {
            return null;
        }
        var Component = type === 'default'
            ? utils_2.getContextComponent(alias) || utils_2.getContextComponent(type)
            : utils_2.getContextComponent(type);
        var isObjectValueEmpty = Object.values(value).filter(function (v) { return utils_1.defined(v); }).length === 0;
        // this can happen if the component does not exist
        if (!Component || isObjectValueEmpty) {
            return null;
        }
        return (<eventDataSection_1.default key={"context-" + alias} type={"context-" + alias} title={<React.Fragment>
            {this.getTitle()}
            {utils_1.defined(type) && type !== 'default' && alias !== type && (<small>({alias})</small>)}
          </React.Fragment>}>
        <Component alias={alias} event={event} data={value}/>
      </eventDataSection_1.default>);
    };
    return Chunk;
}(React.Component));
exports.default = Chunk;
//# sourceMappingURL=chunk.jsx.map